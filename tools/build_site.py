"""Build the Birmingham Healthy Life site.

Reads the story text in content/*.md and the executed notebooks, and writes plain HTML
pages that GitHub Pages serves as they are. Run it from anywhere:

    python tools/build_site.py

Every run clears and rewrites story/, notebooks/, assets/figures/ and assets/nb/,
so nothing stale is left behind. assets/img/ (screenshots) and dashboard/ are left alone.

Story text uses ordinary Markdown plus a few block markers:

    ::: keypoints            a box of the main points, at the top of a chapter
    ::: stats nb04#cellid    a slate panel of numbers; lines are "value | label"
    ::: figure key [wide] nb04#cellid   a notebook figure on a plate;
                             lines "alt: ..." and "caption: ..."
    ::: image file [wide]    a screenshot from assets/img; lines "alt:" and "caption:"
    ::: callout              one plain sentence that matters
    ::: tableau              the Tableau embed with its screenshot
    :::                      closes a block

    ^ nb04#cellid | note     a margin note for the paragraph that follows it

{root} in any link becomes the path back to the site root.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

import markdown
from PIL import Image
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

# Where things are
SITE = Path(__file__).resolve().parent.parent
CONTENT = SITE / "content"
# The site is built from the assessment repository, so it always shows exactly what is marked.
PROJECT = Path(os.environ.get(
    "HLE_PROJECT",
    str(SITE.parent / "Code-Institute-DA-with-AI-Unit-3-Assessment"),
))
NOTEBOOK_DIR = PROJECT / "notebooks"
CLEANED = PROJECT / "data" / "cleaned"
GITHUB_REPO = "https://github.com/TidyWeb/Code-Institute-DA-with-AI-Unit-3-Assessment"
TABLEAU_URL = "https://public.tableau.com/views/BirminghamHLEFinal/Dashboard1"

# The notebooks, in order. Folder names match the assessment repo.
NOTEBOOKS = [
    ("01", "Source exploration", "A — Source Exploration", "01_Source_Exploration.ipynb"),
    ("02", "Data preparation", "B — Data Preparation", "02_Data_Preparation.ipynb"),
    ("03", "Joined table and exploration", "C — Joined Table and Exploration", "03_Joined_Table_and_Exploration.ipynb"),
    ("04", "Hypothesis and neighbour gaps", "D — Hypothesis and Neighbour Gaps", "04_Hypothesis_and_Neighbour_Gaps.ipynb"),
    ("05", "Machine learning", "E — Machine Learning", "05_Machine_Learning.ipynb"),
    ("06", "Hotspots", "F — Hotspots", "06_Hotspots.ipynb"),
]

# Short keys for the saved figure folders
FIGURE_FOLDERS = {
    "wide": "Wide",
    "neighbours": "Neighbours",
    "ml": "Machine Learning",
    "hotspots": "Hotspots",
}

CODE_FOLD_LINES = 6     # code cells longer than this start folded
WEBP_QUALITY = 84
MAX_FIGURE_WIDTH = 1800

FONTS = ("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;600;700"
         "&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&display=swap")


def external_links_in_new_tab(document: str) -> str:
    """Add safe new-tab attributes to external links in generated pages."""
    own_host = "tidyweb.github.io"
    own_path = "/Birmingham-Healthy-Life-Second-Look"

    def update_anchor(match: re.Match[str]) -> str:
        tag = match.group(0)
        href_match = re.search(
            r"""\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""",
            tag,
            flags=re.IGNORECASE,
        )
        if not href_match:
            return tag
        href = next(value for value in href_match.groups() if value is not None)
        if not href.lower().startswith(("http://", "https://")):
            return tag
        parsed = urlsplit(href)
        own_path_match = parsed.path.rstrip("/")
        if ((parsed.hostname or "").lower() == own_host
                and (own_path_match == own_path or own_path_match.startswith(own_path + "/"))):
            return tag
        if re.search(r"\btarget\s*=", tag, flags=re.IGNORECASE):
            return tag

        rel_match = re.search(
            r"""\srel\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""",
            tag,
            flags=re.IGNORECASE,
        )
        if rel_match:
            rel_value = next(value for value in rel_match.groups() if value is not None)
            rel_tokens = rel_value.split()
            for token in ("noopener", "noreferrer"):
                if token not in rel_tokens:
                    rel_tokens.append(token)
            replacement = ' rel="' + " ".join(rel_tokens) + '"'
            tag = tag[:rel_match.start()] + replacement + tag[rel_match.end():]
            insertion = ' target="_blank"'
        else:
            insertion = ' target="_blank" rel="noopener noreferrer"'
        if tag.endswith("/>"):
            return tag[:-2] + insertion + tag[-2:]
        return tag[:-1] + insertion + '>'

    return re.sub(r"<a\b[^>]*>", update_anchor, document, flags=re.IGNORECASE | re.DOTALL)


def nb_slug(num: str, title: str) -> str:
    return f"{num}-" + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


NB_PAGES = {num: f"notebooks/{nb_slug(num, title)}.html" for num, title, _, _ in NOTEBOOKS}
NB_TITLES = {num: title for num, title, _, _ in NOTEBOOKS}
NB_FILES = {file: num for num, _, _, file in NOTEBOOKS}


# ---------- Reading the story content ----------

def read_page_source(path: Path) -> tuple[dict, str]:
    """Split a content file into its header fields and its Markdown body."""
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    if "\n---\n" in text:
        head, body = text.split("\n---\n", 1)
        for line in head.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
    else:
        body = text
    return meta, body


def load_chapters() -> list[dict]:
    chapters = []
    for path in sorted(CONTENT.glob("*.md")):
        meta, body = read_page_source(path)
        if meta.get("layout") == "home":
            continue
        meta["body"] = body
        meta["num"] = meta.get("num", "0").strip()   # "10" or "10A"; a letter makes an in-between chapter
        meta["part"] = meta.get("part", "original").strip()
        if meta["part"] not in {"second-look", "original"}:
            raise ValueError(f"Unknown chapter part in {path.name}: {meta['part']}")
        meta["href"] = f"story/{meta['slug']}.html"
        chapters.append(meta)
    def order(chapter):
        if chapter["part"] == "second-look":
            match = re.fullmatch(r"S(\d+)", chapter["num"], flags=re.IGNORECASE)
            if not match:
                raise ValueError(f"Second-look chapter number must use S followed by a number: {chapter['num']}")
            return 0, int(match.group(1)), ""
        match = re.fullmatch(r"(\d+)([A-Za-z]*)", chapter["num"])
        if not match:
            raise ValueError(f"Original chapter number is not recognised: {chapter['num']}")
        return 1, int(match.group(1)), match.group(2).upper()

    return sorted(chapters, key=order)


# ---------- Figures ----------

def to_webp(src: Path | Image.Image, dest: Path) -> tuple[int, int]:
    """Save an image as WebP, capping its width. Returns the saved size."""
    image = Image.open(src) if isinstance(src, Path) else src
    image = image.convert("RGB")
    if image.width > MAX_FIGURE_WIDTH:
        height = round(image.height * MAX_FIGURE_WIDTH / image.width)
        image = image.resize((MAX_FIGURE_WIDTH, height), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
    return image.size


def story_figure(key: str) -> tuple[str, tuple[int, int]]:
    """Copy a saved notebook figure into the site and return its site path."""
    folder_key, name = key.split("/", 1)
    src = CLEANED / FIGURE_FOLDERS[folder_key] / "figures" / f"{name}.png"
    if not src.exists():
        raise FileNotFoundError(f"Figure not found: {src}")
    rel = f"assets/figures/{folder_key}-{name}.webp"
    size = to_webp(src, SITE / rel)
    return rel, size


# ---------- Source references ----------

def source_link(ref: str, root: str) -> tuple[str, str]:
    """Turn "nb04#cellid" into a link and a label, such as "Notebook 04"."""
    num, _, cell = ref.removeprefix("nb").partition("#")
    href = root + NB_PAGES[num] + (f"#cell-{cell}" if cell else "")
    return href, f"Notebook {num}"


# ---------- Turning story Markdown into HTML ----------

def md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "attr_list", "md_in_html", "sane_lists"])


def inline(text: str) -> str:
    """Markdown for a short phrase, without the paragraph wrapper."""
    out = md(text)
    if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        return out[3:-4]
    return out


def render_block(kind: str, args: list[str], lines: list[str], root: str) -> str:
    fields = {}
    for line in lines:
        if re.match(r"^(alt|caption):", line):
            key, value = line.split(":", 1)
            fields[key] = value.strip()

    if kind == "keypoints":
        return f'<section class="keypoints" aria-label="Key points"><h2>In short</h2>{md(chr(10).join(lines))}</section>'

    if kind == "callout":
        return f'<p class="callout">{inline(" ".join(lines))}</p>'

    if kind == "stats":
        items = []
        for line in lines:
            if "|" in line:
                value, label = [part.strip() for part in line.split("|", 1)]
                items.append(f"<div><dt>{html.escape(value)}</dt><dd>{inline(label)}</dd></div>")
        source = ""
        if args:
            href, label = source_link(args[0], root)
            source = f'<p class="from">From <a href="{href}">{label}</a></p>'
        return f'<div class="stats"><dl>{"".join(items)}</dl>{source}</div>'

    if kind in ("figure", "image"):
        wide = "wide" in args
        if kind == "figure":
            rel, (w, h) = story_figure(args[0])
        else:
            if not fields.get("alt") or not fields.get("caption"):
                raise ValueError("Image blocks require both alt: and caption: lines")
            asset_root = (SITE / "assets" / "img").resolve()
            image_path = (asset_root / args[0]).resolve()
            try:
                image_rel = image_path.relative_to(asset_root)
            except ValueError as exc:
                raise ValueError(f"Image must be inside assets/img: {args[0]}") from exc
            rel = (Path("assets") / "img" / image_rel).as_posix()
            if not image_path.is_file():
                raise FileNotFoundError(f"Image not found: {image_path}")
            if image_path.suffix.lower() == ".svg":
                if not image_rel.parts or image_rel.parts[0] != "second-look":
                    raise ValueError("SVG image blocks must be stored in assets/img/second-look/")
                svg = image_path.read_text(encoding="utf-8")
                view_box = re.search(r"\bviewBox=[\"']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)[\"']", svg)
                if not view_box:
                    raise ValueError(f"SVG needs a numeric viewBox: {image_path}")
                w, h = round(float(view_box.group(1))), round(float(view_box.group(2)))
            else:
                with Image.open(image_path) as im:
                    w, h = im.size
        refs = [a for a in args[1:] if a.startswith("nb")]
        src_html = ""
        if refs:
            href, label = source_link(refs[0], root)
            src_html = f' <span class="src">From <a href="{href}">{label}</a>.</span>'
        caption = inline(fields.get("caption", ""))
        classes = "plate" + (" wide" if wide else "") + (" photo" if kind == "image" else "")
        return (f'<figure class="{classes}"><div class="sheet"><img src="{root}{rel}" width="{w}" height="{h}" '
                f'alt="{html.escape(fields.get("alt", ""))}" loading="lazy"></div>'
                f'<figcaption>{caption}{src_html}</figcaption></figure>')

    if kind == "tableau":
        shot = "assets/img/tableau-dashboard.webp"
        embed = TABLEAU_URL + "?:showVizHome=no&:embed=true"
        img = ""
        if (SITE / shot).exists():
            with Image.open(SITE / shot) as im:
                w, h = im.size
            img = f'<img src="{root}{shot}" width="{w}" height="{h}" alt="Screenshot of my Tableau Public dashboard">'
        return (f'<div class="embed"><div class="frame">{img}'
                f'<button class="btn btn-ink load" data-embed="{embed}" data-title="Birmingham HLE on Tableau Public">'
                f'Load the live Tableau dashboard</button></div>'
                f'<p class="nb-meta"><a href="{TABLEAU_URL}">Open it on Tableau Public</a></p></div>')

    raise ValueError(f"Unknown block: {kind}")


def render_story(body: str, root: str) -> str:
    """Process block markers and margin notes, then Markdown for everything else."""
    body = body.replace("{root}", root)
    out: list[str] = []
    buffer: list[str] = []
    lines = body.splitlines()
    i = 0

    def flush():
        if buffer:
            out.append(md("\n".join(buffer)))
            buffer.clear()

    while i < len(lines):
        line = lines[i]
        opener = re.match(r"^:::\s*(\w+)\s*(.*)$", line)
        if opener:
            flush()
            kind, args = opener.group(1), opener.group(2).split()
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                block.append(lines[i])
                i += 1
            out.append(render_block(kind, args, block, root))
            i += 1
            continue
        note = re.match(r"^\^\s*(nb\d\d(?:#[\w-]+)?)\s*\|\s*(.+)$", line)
        if note:
            flush()
            href, label = source_link(note.group(1), root)
            out.append(f'<aside class="note"><a href="{href}">{label}</a>{inline(note.group(2))}</aside>')
            i += 1
            continue
        buffer.append(line)
        i += 1
    flush()
    return "\n".join(out)


# ---------- The page shell ----------

def sidebar(chapters: list[dict], active: str, root: str) -> str:
    def item(href: str, num: str, title: str, external: bool = False) -> str:
        current = ' aria-current="page"' if href == active else ""
        ext = ""
        return f'<li><a href="{root}{href}"{current}><span class="n">{num}</span><span>{html.escape(title)}</span>{ext}</a></li>'

    story = "".join(
        f'<div class="nav-group"><h2>{label}</h2><ol>'
        + "".join(item(c["href"], str(c["num"]), c["title"]) for c in chapters if c["part"] == part)
        + "</ol></div>"
        for label, part in (
            ("A second look (Unit 3)", "second-look"),
            ("The original project (Unit 2)", "original"),
        )
    )
    tools = (item("dashboard/", "", "My dashboard", True)
             + '<li><span class="soon"><span class="n"></span><span>3D hotspots, in progress</span></span></li>')
    nbs = "".join(item(NB_PAGES[num], num, title) for num, title, _, _ in NOTEBOOKS)
    return f"""
<header class="sidebar" id="top">
  <a class="sidebar-logo" href="https://github.com/TidyWeb" title="Tidy Web on GitHub"><img src="{root}assets/img/tidyweb-logo.png" width="120" height="120" alt="Tidy Web on GitHub"></a>
  <a class="site-name" href="{root}index.html">Birmingham Healthy Life<small>Years in good health, area by area</small></a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Contents</button>
  <nav class="nav" id="site-nav" aria-label="Site contents">
    {story}
    <div class="nav-group"><h2>Tools</h2><ul>{tools}</ul></div>
    <div class="nav-group"><h2>The notebooks</h2><ol>{nbs}</ol></div>
  </nav>
</header>"""


def asset_version() -> str:
    """A short fingerprint of the stylesheet, so browsers reload it whenever it changes."""
    import hashlib
    return hashlib.md5((SITE / "assets" / "site.css").read_bytes()).hexdigest()[:8]


def page(title: str, body: str, active: str, root: str, chapters: list[dict], description: str = "") -> str:
    document = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Birmingham Healthy Life</title>
<meta name="description" content="{html.escape(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="icon" type="image/png" href="{root}assets/img/favicon.png">
<link rel="stylesheet" href="{root}assets/site.css?v={asset_version()}">
</head>
<body>
<a class="skip" href="#main">Skip to the text</a>
<div class="shell">
{sidebar(chapters, active, root)}
<main class="content" id="main">
{body}
</main>
</div>
<script src="{root}assets/site.js"></script>
</body>
</html>
"""
    return external_links_in_new_tab(document)


def pager(chapters: list[dict], index: int, root: str) -> str:
    parts = []
    if index > 0:
        prev = chapters[index - 1]
        parts.append(f'<a class="prev" href="{root}{prev["href"]}"><small>Previous</small><strong>{prev["num"]}. {html.escape(prev["title"])}</strong></a>')
    else:
        parts.append(f'<a class="prev" href="{root}index.html"><small>Previous</small><strong>Home</strong></a>')
    if index < len(chapters) - 1:
        nxt = chapters[index + 1]
        parts.append(f'<a class="next" href="{root}{nxt["href"]}"><small>Next</small><strong>{nxt["num"]}. {html.escape(nxt["title"])}</strong></a>')
    return f'<nav class="pager" aria-label="Chapters">{"".join(parts)}</nav>'


def build_chapters(chapters: list[dict]) -> None:
    root = "../"
    for index, chapter in enumerate(chapters):
        head = (f'<header class="chapter-head"><p class="chapter-num">Chapter {chapter["num"]}</p>'
                f'<h1>{html.escape(chapter["title"])}</h1>'
                + (f'<p class="standfirst">{html.escape(chapter["standfirst"])}</p>' if chapter.get("standfirst") else "")
                + "</header>")
        body = f'<article class="page">{head}{render_story(chapter["body"], root)}{pager(chapters, index, root)}</article>'
        out = SITE / chapter["href"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(chapter["title"], body, chapter["href"], root, chapters, chapter.get("standfirst", "")), encoding="utf-8")


def build_home(chapters: list[dict]) -> None:
    meta, body = read_page_source(CONTENT / "00-home.md")
    root = ""
    hero, _, rest = body.partition("<!-- contents -->")
    toc = "".join(
        f'<section class="toc-part"><h2>{label}</h2><ol class="toc">'
        + "".join(
            f'<li><a href="{c["href"]}"><span class="n">{c["num"]}</span><strong>{html.escape(c["title"])}</strong>'
            f'<span class="d">{html.escape(c.get("summary", ""))}</span></a></li>'
            for c in chapters if c["part"] == part
        )
        + "</ol></section>"
        for label, part in (
            ("A second look (Unit 3)", "second-look"),
            ("The original project (Unit 2)", "original"),
        )
    )
    contents = render_story(rest, root).replace("<!-- toc -->", toc).replace("<p>&lt;!-- toc --&gt;</p>", toc)
    html_body = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Birmingham Healthy Life</title>
<meta name="description" content="{html.escape(meta.get('description', ''))}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="stylesheet" href="assets/site.css?v={asset_version()}">
</head>
<body>
<a class="skip" href="#contents">Skip to the contents</a>
<header class="home-hero">
  <div class="hero-card">{render_story(hero, root)}</div>
</header>
<main class="home-contents" id="contents">{contents}</main>
<footer class="home-foot"><a class="logo" href="https://github.com/TidyWeb" title="Tidy Web on GitHub"><img src="assets/img/tidyweb-logo.png" width="36" height="36" alt="Tidy Web on GitHub"></a>{md(meta.get('footer', ''))}</footer>
</body>
</html>
"""
    (SITE / "index.html").write_text(external_links_in_new_tab(html_body), encoding="utf-8")


# ---------- Notebook pages ----------

FORMATTER = HtmlFormatter(nowrap=True)
LEXER = PythonLexer()


MAX_LINKED_FILE = 15 * 1024 * 1024   # files a notebook links to are copied in up to this size


def rewrite_local_links(text: str, folder: str, root: str) -> str:
    """Links from a notebook to local files (such as a YData report) are copied into the site.

    A link whose file can't be found, or is too big to publish, keeps its text and loses the link,
    so the page never carries a dead link.
    """
    from urllib.parse import quote, unquote

    def repl(match):
        label, target = match.group(1), match.group(2)
        if re.match(r"^(https?:|mailto:|#)", target) or ".ipynb" in target \
                or target.startswith((root + "notebooks/", root + "assets/")):
            return match.group(0)
        path = (NOTEBOOK_DIR / folder / unquote(target.split("#")[0])).resolve()
        if path.is_file() and path.stat().st_size <= MAX_LINKED_FILE:
            dest = SITE / "assets" / "files" / path.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
            return f"[{label}]({root}assets/files/{quote(path.name)})"
        print(f"  unlinked in {folder}: {target}")
        return label

    return re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", repl, text)


def rewrite_notebook_links(text: str, root: str) -> str:
    """Links between notebooks point at the site's notebook pages."""
    def repl(match):
        target = match.group(2)
        name = target.split("/")[-1].split("#")[0]
        name = re.sub(r"%20", " ", name)
        for file, num in NB_FILES.items():
            if name.endswith(file):
                return f"]({root}{NB_PAGES[num]})"
        return match.group(0)
    return re.sub(r"\]\((\.\./)?([^)]+?\.ipynb[^)]*)\)", repl, text)


def render_output(output: dict, num: str, cell_id: str, k: int, root: str, folder: str) -> str:
    kind = output.get("output_type")
    if kind == "stream":
        return f'<pre>{html.escape("".join(output.get("text", "")))}</pre>'
    if kind == "error":
        return f'<pre>{html.escape(output.get("ename", ""))}: {html.escape(output.get("evalue", ""))}</pre>'
    data = output.get("data", {})
    if "image/png" in data:
        import base64, io
        raw = base64.b64decode("".join(data["image/png"]))
        image = Image.open(io.BytesIO(raw))
        rel = f"assets/nb/{num}-{cell_id}-{k}.webp"
        w, h = to_webp(image, SITE / rel)
        alt = f"Output of a code cell in Notebook {num}"
        wide = " nb-wide" if w > 1100 else ""
        return (f'<figure class="plate{wide}"><div class="sheet"><img src="{root}{rel}" width="{w}" height="{h}" '
                f'alt="{alt}" loading="lazy"></div></figure>')
    if "text/html" in data:
        fragment = "".join(data["text/html"])
        fragment = re.sub(r"<style[^>]*>.*?</style>", "", fragment, flags=re.S)
        return f'<div class="table-wrap">{fragment}</div>'
    if "text/markdown" in data:
        return md(rewrite_local_links(rewrite_notebook_links("".join(data["text/markdown"]), root), folder, root))
    if "text/plain" in data:
        return f'<pre>{html.escape("".join(data["text/plain"]))}</pre>'
    return ""


def build_notebook(num: str, title: str, folder: str, file: str, chapters: list[dict]) -> None:
    root = "../"
    notebook = json.loads((NOTEBOOK_DIR / folder / file).read_text(encoding="utf-8"))
    cells = []
    for index, cell in enumerate(notebook["cells"]):
        cell_id = cell.get("id") or f"c{index}"
        source = "".join(cell.get("source", ""))
        if cell["cell_type"] == "markdown":
            cells.append(f'<section class="nb-cell nb-md" id="cell-{cell_id}">{md(rewrite_local_links(rewrite_notebook_links(source, root), folder, root))}</section>')
            continue
        if cell["cell_type"] != "code":
            continue
        code = highlight(source, LEXER, FORMATTER) if source.strip() else ""
        line_count = source.count("\n") + 1
        if not code:
            code_html = ""
        elif line_count > CODE_FOLD_LINES:
            code_html = f'<details><summary>Show code ({line_count} lines)</summary><pre class="hl">{code}</pre></details>'
        else:
            code_html = f'<pre class="hl">{code}</pre>'
        outputs = "".join(render_output(o, num, cell_id, k, root, folder) for k, o in enumerate(cell.get("outputs", [])))
        cells.append(f'<section class="nb-cell nb-code" id="cell-{cell_id}">{code_html}'
                     + (f'<div class="nb-out">{outputs}</div>' if outputs else "") + "</section>")

    from urllib.parse import quote
    github = f"{GITHUB_REPO}/blob/main/notebooks/{quote(folder)}/{file}"
    head = (f'<header class="chapter-head"><p class="chapter-num">Notebook {num}, a read-only record</p></header>'
            f'<p class="nb-meta"><span>Rendered from the executed notebook. Nothing here runs in your browser.</span>'
            f'<a href="{github}">See it on GitHub</a></p>')
    body = f'<article class="page notebook">{head}{"".join(cells)}</article>'
    out = SITE / NB_PAGES[num]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(f"Notebook {num}: {title}", body, NB_PAGES[num], root, chapters,
                        f"Notebook {num}, {title}, rendered as a read-only page."), encoding="utf-8")


# ---------- The dashboard's way back ----------

BACK_LINK = (
    '<a href="../story/my-dashboard.html" id="back-to-story" '
    # Go back to the exact page the reader came from; if they arrived directly, go to the dashboard chapter
    'onclick="if(document.referrer&&document.referrer.indexOf(location.origin)===0&&history.length>1){history.back();return false;}" '
    'style="position:fixed;left:50%;top:14px;transform:translateX(-50%);z-index:2000;background:#172b35f2;color:#f3f4eb;'
    'font:600 14px/1 system-ui,-apple-system,Segoe UI,sans-serif;padding:10px 14px;border-radius:8px;border:1px solid #ffffff25;'
    'text-decoration:none;box-shadow:0 6px 18px rgba(0,0,0,.25)">Back</a>'
)


def dashboard_back_link() -> None:
    """Put the Back button into the dashboard page, replacing any earlier version of it."""
    page_path = SITE / "dashboard" / "index.html"
    if not page_path.exists():
        print("  no dashboard/index.html found")
        return
    text = page_path.read_text(encoding="utf-8")
    text = re.sub(r'<a [^>]*id="back-to-story"[^>]*>.*?</a>\n?', "", text, flags=re.S)
    assert text.count("</body>") == 1
    page_path.write_text(text.replace("</body>", BACK_LINK + "\n</body>"), encoding="utf-8")


# ---------- Run ----------

def clean() -> None:
    for name in ("story", "notebooks", "assets/figures", "assets/nb", "assets/files"):
        target = SITE / name
        if target.exists():
            shutil.rmtree(target)


def main() -> None:
    clean()
    chapters = load_chapters()
    build_chapters(chapters)
    build_home(chapters)
    for num, title, folder, file in NOTEBOOKS:
        build_notebook(num, title, folder, file, chapters)
    dashboard_back_link()
    pages = len(chapters) + 1 + len(NOTEBOOKS)
    figures = len(list((SITE / "assets/figures").glob("*.webp")))
    nb_images = len(list((SITE / "assets/nb").glob("*.webp")))
    print(f"Built {pages} pages: home, {len(chapters)} chapters, {len(NOTEBOOKS)} notebooks.")
    print(f"Figures: {figures} story figures, {nb_images} notebook images.")


if __name__ == "__main__":
    main()
