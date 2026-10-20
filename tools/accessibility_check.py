"""Run a desktop accessibility spot check on the built Unit 3 site."""

from __future__ import annotations

import argparse
import asyncio
import re
from pathlib import Path

from playwright.async_api import async_playwright


def colour_tokens(css: str) -> dict[str, str]:
    root = re.search(r":root\s*\{([^}]+)\}", css, flags=re.S)
    if not root:
        raise ValueError("Could not find the site.css :root token block")
    return dict(re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\b", root.group(1)))


def rgb(hex_colour: str) -> tuple[int, int, int]:
    value = hex_colour.lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if len(value) != 6:
        raise ValueError(f"Unsupported colour token: {hex_colour}")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def luminance(hex_colour: str) -> float:
    channels = [channel / 255 for channel in rgb(hex_colour)]
    linear = [value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4
              for value in channels]
    return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]


def contrast(first: str, second: str) -> float:
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + .05) / (low + .05)


def contrast_rows(css: str) -> list[tuple[str, float, float, bool]]:
    tokens = colour_tokens(css)
    pairs = [
        ("Main body text · ink on paper · normal", "ink", "paper", 4.5),
        ("Main reading panel · ink on plate · normal", "ink", "plate", 4.5),
        ("Muted main text · ink-muted on plate · normal", "ink-muted", "plate", 4.5),
        ("Links · teal on paper · normal", "teal", "paper", 4.5),
        ("Links · teal on plate · normal", "teal", "plate", 4.5),
        ("Keypoints text · ink on paper-deep · normal", "ink", "paper-deep", 4.5),
        ("Keypoints muted text · ink-muted on paper-deep · normal", "ink-muted", "paper-deep", 4.5),
        ("Keypoints links · teal on paper-deep · normal", "teal", "paper-deep", 4.5),
        ("Sidebar links · ink on slate · normal", "ink", "slate", 4.5),
        ("Sidebar muted labels · on-slate-muted on slate · normal", "on-slate-muted", "slate", 4.5),
        ("Sidebar active number · accent on plate · normal", "accent", "plate", 4.5),
        ("Footer text · ink-muted on paper-deep · normal", "ink-muted", "paper-deep", 4.5),
        ("Footer links · ink on paper-deep · normal", "ink", "paper-deep", 4.5),
        ("Main h1 · ink on plate · large", "ink", "plate", 3.0),
    ]
    output = []
    for label, foreground, background, threshold in pairs:
        ratio = contrast(tokens[foreground], tokens[background])
        output.append((label, ratio, threshold, ratio >= threshold))
    return output


def built_pages(site: Path) -> list[Path]:
    paths = [site / "index.html"]
    paths.extend(sorted((site / "story").glob("*.html")))
    paths.extend(sorted((site / "notebooks").glob("*.html")))
    paths.append(site / "dashboard" / "index.html")
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Built page missing: " + ", ".join(map(str, missing)))
    return paths


def page_url(base_url: str, site: Path, path: Path) -> str:
    relative = path.relative_to(site).as_posix()
    return base_url.rstrip("/") + ("/" + relative if relative != "index.html" else "/")


async def describe_focus(page) -> dict[str, str | bool]:
    return await page.evaluate("""() => {
      const el = document.activeElement;
      if (!el || el === document.body) return {tag: 'body', label: '', isSkip: false,
        inNav: false, inMain: false, isControl: false, visible: false, focusVisible: false};
      const css = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return {
        tag: el.tagName.toLowerCase(),
        label: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || el.getAttribute('href') || '').trim().replace(/\\s+/g, ' ').slice(0, 72),
        isSkip: el.matches('a.skip'),
        inNav: Boolean(el.closest('nav, .nav-group, .toc, [aria-label*="navigation" i]')),
        inMain: Boolean(el.closest('main, #main, #contents, #app')),
        isControl: el.matches('button, input, select, textarea, summary, [role="button"]'),
        visible: rect.width > 0 && rect.height > 0 && css.visibility !== 'hidden' && css.display !== 'none',
        focusVisible: el.matches(':focus-visible')
      };
    }""")


async def keyboard_check(browser, url: str, label: str, limit: int = 80):
    page = await browser.new_page(viewport={"width": 1440, "height": 1000})
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.evaluate("document.activeElement.blur()")
    sequence = []
    for _ in range(limit):
        await page.keyboard.press("Tab")
        focus = await describe_focus(page)
        sequence.append(focus)
        if focus["tag"] == "body":
            break
        if focus["isSkip"] and len(sequence) > 1:
            break
    skip_first = bool(sequence and sequence[0]["isSkip"])
    nav_seen = any(item["inNav"] for item in sequence[1:])
    main_control_seen = any(
        item["inMain"] and (item["isControl"] or item["tag"] == "a")
        for item in sequence[1:]
    )
    focused_items = [item for item in sequence if item["visible"]]
    focus_visible = bool(focused_items) and all(item["focusVisible"] for item in focused_items)
    await page.close()
    return {
        "label": label,
        "url": url,
        "sequence": sequence,
        "skip_first": skip_first,
        "nav_seen": nav_seen,
        "main_control_seen": main_control_seen,
        "focus_visible": focus_visible,
    }


async def run(site: Path, base_url: str) -> str:
    pages = built_pages(site)
    issues: list[str] = []
    page_rows: list[dict[str, object]] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, channel="chrome")
        page = await browser.new_page(viewport={"width": 1440, "height": 1000})
        for path in pages:
            url = page_url(base_url, site, path)
            response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            if response is None or response.status != 200:
                issues.append(f"HTTP {response.status if response else 'no response'}: {path.relative_to(site)}")
            audit = await page.evaluate("""() => ({
              title: document.title.trim(),
              lang: document.documentElement.getAttribute('lang'),
              // Count only headings that are shown: the dashboard holds one heading per view and hides the other.
              h1Count: [...document.querySelectorAll('h1')].filter(h => h.getClientRects().length > 0).length,
              images: Array.from(document.images).map(img => ({src: img.getAttribute('src') || '', alt: img.getAttribute('alt')}))
            })""")
            # A missing alt is a fault. An empty alt (alt="") marks a decorative image that screen readers
            # should skip, such as a map tile, so it is counted separately rather than reported as missing.
            missing_alt = [image["src"] for image in audit["images"] if not isinstance(image["alt"], str)]
            decorative = [image["src"] for image in audit["images"]
                          if isinstance(image["alt"], str) and not image["alt"].strip()]
            if missing_alt:
                issues.append(f"Missing/empty alt in {path.relative_to(site)}: {', '.join(missing_alt)}")
            if not audit["title"]:
                issues.append(f"Missing title: {path.relative_to(site)}")
            if audit["lang"] != "en-GB":
                issues.append(f"lang is {audit['lang']!r}, expected 'en-GB': {path.relative_to(site)}")
            if audit["h1Count"] != 1:
                issues.append(f"Found {audit['h1Count']} h1 elements: {path.relative_to(site)}")
            page_rows.append({
                "path": path.relative_to(site).as_posix(),
                "title": audit["title"], "lang": audit["lang"],
                "h1": audit["h1Count"], "images": len(audit["images"]),
                "missing_alt": missing_alt, "decorative": len(decorative),
            })
        await page.close()

        keyboard = []
        for label, relative in (("Home", ""), ("S1", "story/s1-why-a-second-look.html"), ("Dashboard", "dashboard/")):
            url = base_url.rstrip("/") + "/" + relative
            result = await keyboard_check(browser, url, label)
            keyboard.append(result)
            if not result["skip_first"]:
                issues.append(f"{label}: Tab did not reach the skip link first")
            if not result["nav_seen"]:
                issues.append(f"{label}: sampled Tab sequence did not reach navigation")
            if not result["main_control_seen"]:
                issues.append(f"{label}: sampled Tab sequence did not reach a main control/link")
            if not result["focus_visible"]:
                issues.append(f"{label}: sampled keyboard focus was not consistently visible")
        await browser.close()

    css = (site / "assets" / "site.css").read_text(encoding="utf-8")
    ratios = contrast_rows(css)
    report = [
        "# Accessibility check — 2026-10-17", "",
        "Desktop check at 1440 × 1000 using Playwright with the installed Chrome browser. The check covers the home page, every generated story and notebook page, and the dashboard. It checks image alt text, page title, one h1, `lang=\"en-GB\"`, sampled keyboard order and visible focus, plus selected colour-token pairs from `assets/site.css`.", "",
        f"Pages checked: {len(page_rows)}. Browser checks: {'PASS' if not issues else 'REVIEW REQUIRED'}.", "",
        "## Page checks", "",
        "| Page | Title | lang | h1 count | Images | Decorative (empty alt) | Missing alt |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for row in page_rows:
        missing = ", ".join(row["missing_alt"]) or "None"
        report.append(f"| `{row['path']}` | {'Present' if row['title'] else 'Missing'} | `{row['lang']}` | {row['h1']} | {row['images']} | {row['decorative']} | {missing} |")
    report.extend(["", "## Keyboard sample", "", "| Page | First Tab | Navigation reached | Main control/link reached | Focus visible | Sampled sequence |", "|---|---|---|---|---|---|"])
    for result in keyboard:
        visible_sequence = result["sequence"]
        if len(visible_sequence) > 18:
            visible_sequence = visible_sequence[:10] + [{"tag": "…", "label": ""}] + visible_sequence[-5:]
        sequence = " → ".join(f"{item['tag']} {item['label']}".strip() for item in visible_sequence)
        report.append(f"| {result['label']} | {'Pass' if result['skip_first'] else 'Fail'} | {'Yes' if result['nav_seen'] else 'No'} | {'Yes' if result['main_control_seen'] else 'No'} | {'Yes' if result['focus_visible'] else 'No'} | {sequence} |")
    report.extend(["", "## Contrast from `assets/site.css` colour tokens", "", "WCAG AA thresholds: 4.5:1 for normal text and 3:1 for large text. No palette changes were made.", "", "| Text and background | Ratio | Threshold | Result |", "|---|---:|---:|---|"])
    for label, ratio, threshold, passed in ratios:
        report.append(f"| {label} | {ratio:.2f}:1 | {threshold:.1f}:1 | {'Pass' if passed else 'Below threshold'} |")
    failures = [row for row in ratios if not row[3]]
    report.extend(["", "## Findings and fixes", ""])
    report.append("- Missing image alt text: none found." if not any("alt" in issue.lower() for issue in issues) else "- Missing image alt text was reported above; fix only clear cases before publication.")
    report.append("- Page metadata: the dashboard language tag was corrected from `en` to `en-GB`; all checked pages now have a title, exactly one h1 and the required language tag." if not any("title" in issue.lower() or "lang" in issue.lower() or "h1" in issue.lower() for issue in issues) else "- Page metadata findings are listed above.")
    report.append("- Contrast failures: none." if not failures else "- Contrast items below threshold are listed in the table for Phil; the colours were not changed.")
    report.append("- Keyboard findings: none." if not any(any(word in issue.lower() for word in ("tab", "navigation", "focus")) for issue in issues) else "- Keyboard findings are listed above for Phil to review.")
    if issues:
        report.extend(["", "### Browser findings", ""])
        report.extend(f"- {issue}" for issue in issues)
    return "\n".join(report) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--base-url", default="http://127.0.0.1:8766")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = asyncio.run(run(args.site.resolve(), args.base_url))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(result, encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
