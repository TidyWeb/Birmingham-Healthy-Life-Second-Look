#!/usr/bin/env python3
"""Report loaded or overclaiming language in story Markdown and dashboard text."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
CONTENT = SITE / "content"
TEMPLATE = SITE / "tools" / "dashboard" / "template.html"

TERMS = [
    ("worst", re.compile(r"\bworst\b", re.IGNORECASE)),
    ("best", re.compile(r"\bbest\b", re.IGNORECASE)),
    ("unhealthy", re.compile(r"\bunhealthy\b", re.IGNORECASE)),
    ("deprived area(s)", re.compile(r"\bdeprived areas?\b", re.IGNORECASE)),
    ("problem area(s)", re.compile(r"\bproblem areas?\b", re.IGNORECASE)),
    ("poor area(s)", re.compile(r"\bpoor areas?\b", re.IGNORECASE)),
    ("causes", re.compile(r"\bcauses\b", re.IGNORECASE)),
    ("caused by", re.compile(r"\bcaused\s+by\b", re.IGNORECASE)),
    ("due to", re.compile(r"\bdue\s+to\b", re.IGNORECASE)),
    ("because of", re.compile(r"\bbecause\s+of\b", re.IGNORECASE)),
    ("proves", re.compile(r"\bproves\b", re.IGNORECASE)),
    ("explains", re.compile(r"\bexplains\b", re.IGNORECASE)),
    ("will", re.compile(r"\bwill\b", re.IGNORECASE)),
    ("always", re.compile(r"\balways\b", re.IGNORECASE)),
    ("never", re.compile(r"\bnever\b", re.IGNORECASE)),
    ("all residents", re.compile(r"\ball residents\b", re.IGNORECASE)),
    ("people in X are", re.compile(
        r"\bpeople\s+in\s+[\w'’.-]+(?:\s+[\w'’.-]+){0,2}\s+are\b",
        re.IGNORECASE,
    )),
]


class VisibleHTMLText(HTMLParser):
    """Collect text nodes visible in the rendered document, excluding code and styling."""

    HIDDEN = {"head", "script", "style", "template", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hidden_depth = 0
        self.rows: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in self.HIDDEN:
            self.hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.HIDDEN and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.hidden_depth or not data.strip():
            return
        start_line = self.getpos()[0]
        for offset, line in enumerate(data.splitlines() or [data]):
            if line.strip():
                self.rows.append((start_line + offset, line.strip()))


def lines_for(path: Path) -> list[tuple[int, str]]:
    if path.suffix.lower() != ".html":
        return [(number, line.strip()) for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ) if line.strip()]
    parser = VisibleHTMLText()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.rows


def find_hits(path: Path) -> list[tuple[int, str, str]]:
    hits = []
    for line_no, line in lines_for(path):
        for name, pattern in TERMS:
            for match in pattern.finditer(line):
                left = max(0, match.start() - 70)
                right = min(len(line), match.end() + 90)
                context = line[left:right].replace("\t", " ")
                hits.append((line_no, name, context))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="write machine-readable JSON")
    args = parser.parse_args()
    paths = sorted(CONTENT.glob("*.md")) + [TEMPLATE]
    results = []
    for path in paths:
        for line, term, context in find_hits(path):
            results.append({"file": path.relative_to(SITE).as_posix(), "line": line,
                            "term": term, "context": context})
    if args.json:
        import json
        import sys
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        for hit in results:
            print(f'{hit["file"]}:{hit["line"]}: [{hit["term"]}] {hit["context"]}')
        print(f"\n{len(results)} hits across {len(paths)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
