"""The read-only Signal Box shown on the story pages.

The questions are a fixed copy of Signal Box from the Ethical Considerations in AI
guide (signal_box_questions.json). The answers come from the assessment repo's
data/ethics/unit3_screen_results.csv. build_site.py calls write_data() to save
assets/signal-box/signal-box-data.js, and figure() to place a board on a page:

    ::: signalbox full                 the whole Signal Box (The method)
    ::: signalbox checkpoints          every lamp by checkpoint, Unit 2 screen
    ::: signalbox stages               Unit 2 concerns by project stage
    ::: signalbox before-after [wide]  Unit 2 screen beside the Unit 3 re-test
    ::: signalbox stage S7             one stage's questions, before and after
"""

from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path

from ethics_register import STAGE_CLEAR_QUESTIONS

SITE = Path(__file__).resolve().parent.parent
QUESTIONS = Path(__file__).resolve().parent / "signal_box_questions.json"
DATA_JS = SITE / "assets" / "signal-box" / "signal-box-data.js"
OWN_STORY = "https://tidyweb.github.io/Birmingham-Healthy-Life-Second-Look/story/"
GUIDE_URL = "https://tidyweb.github.io/ethical-considerations-in-ai/#screening-tool"
STAGE_FILES = {
    "S1": "s4-stage-1-choosing-sources.html",
    "S2": "stage-2-preparing-and-aggregating.html",
    "S3": "stage-3-joined-table.html",
    "S4": "stage-4-hypothesis-test.html",
    "S5": "stage-5-machine-learning.html",
    "S6": "stage-6-hotspots.html",
    "S7": "stage-7-dashboards-and-site.html",
}
METHOD_HREF = "s2-the-method.html#sbx"

# Phil's decision on the lamps that stay orange (20 October 2026).
DECISION = {
    "intro": "I've published with three concerns still open. I looked at each one and decided to go ahead anyway; this is why.",
    "items": [
        {"n": 4, "title": "Q4. The benefit is mine; any cost falls on others.",
         "text": "If anyone pays a cost it's the people living in the areas with the fewest years in good health, through stigma. I accept that as the cost of trying to get to the truth about these differences, and I've kept it down with broad labels, honest uncertainty and a policy on naming places."},
        {"n": 18, "title": "Q18. The people affected weren't involved.",
         "text": "The study covers 660 areas and several million people. There's no practical way to involve them all, and publishing area-level statistics doesn't need their permission. Three Birmingham readers are testing the site, which helps, but three people can't speak for everyone."},
        {"n": 21, "title": "Q21. It hasn't been tested in real use.",
         "text": "This is a course project, built to be assessed, not for anyone to rely on. It won't ever be used for real, so this lamp can't honestly turn yellow."},
    ],
}


def _lamp_now(row: dict) -> str:
    if row["lamp"] == "no_flag":
        return "g"
    return "y" if row["after_status"] == "investigated_and_recorded" else "o"


def build_data(project: Path, chapters: list[dict]) -> dict:
    """Join the fixed questions to the recorded answers. Fails loudly if anything doesn't line up."""
    groups = json.loads(QUESTIONS.read_text(encoding="utf-8"))["groups"]
    rows = {int(r["q"]): r for r in csv.DictReader((project / "data/ethics/unit3_screen_results.csv").open(encoding="utf-8"))}
    if len(rows) != 27:
        raise ValueError(f"Expected 27 Signal Box answers, found {len(rows)}")
    titles = {Path(c["href"]).name: c["title"] for c in chapters if c["href"].startswith("story/")}

    out_groups = []
    for g in groups:
        qs = []
        for q in g["qs"]:
            r = rows[q["n"]]
            if r["checkpoint"] != g["id"]:
                raise ValueError(f"Q{q['n']} is in checkpoint {r['checkpoint']} in the CSV, {g['id']} in the questions")
            where = None
            url = r.get("evidence_url", "").strip()
            if url.startswith(OWN_STORY):
                href = url[len(OWN_STORY):]
                if href.split("#")[0] not in titles:
                    raise ValueError(f"Q{q['n']} links to a page that doesn't exist: {href}")
                where = {"href": href, "label": titles[href.split("#")[0]], "ext": False}
            elif url:
                raise ValueError(f"Q{q['n']} links outside this site: {url}")
            stages = [s for s in r["stages"].split(";") if re.fullmatch(r"S[1-7]", s)]
            if not stages:
                stages = [s for s, ns in STAGE_CLEAR_QUESTIONS.items() if q["n"] in ns]
            qs.append({
                "n": q["n"], "g": g["id"], "q": q["q"], "legal": q["legal"],
                "lamp": _lamp_now(r), "before": "g" if r["lamp"] == "no_flag" else "o", "stages": stages,
                "evidence": [p.strip() for p in r["evidence"].split("\n") if p.strip()],
                "action": r["action"].strip(), "where": where,
            })
        out_groups.append({"id": g["id"], "name": g["name"], "qs": qs})

    flat = [q for g in out_groups for q in g["qs"]]
    still_open = sorted(q["n"] for q in flat if q["lamp"] == "o")
    if still_open != [item["n"] for item in DECISION["items"]]:
        raise ValueError(f"Open lamps {still_open} don't match the recorded decision")
    decision = {"intro": DECISION["intro"],
                "items": [dict(item, g=next(q["g"] for q in flat if q["n"] == item["n"])) for item in DECISION["items"]]}
    stages = [{"id": s, "href": f, "title": titles[f]} for s, f in STAGE_FILES.items()]
    return {"groups": out_groups, "decision": decision, "stages": stages, "methodHref": METHOD_HREF}


def write_data(project: Path, chapters: list[dict]) -> dict:
    data = build_data(project, chapters)
    DATA_JS.parent.mkdir(parents=True, exist_ok=True)
    DATA_JS.write_text("window.SBX_DATA = " + json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/") + ";\n",
                       encoding="utf-8")
    return data


def asset_version() -> str:
    """A short fingerprint of the Signal Box files, so browsers reload them whenever they change."""
    import hashlib
    digest = hashlib.md5()
    for name in ("signal-box.css", "signal-box.js", "signal-box-data.js"):
        path = DATA_JS.parent / name
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()[:8]


def _counts(qs: list[dict], field: str) -> dict[str, int]:
    out = {"o": 0, "y": 0, "g": 0}
    for q in qs:
        out[q[field]] += 1
    return out


def _n(count: int, one: str, many: str) -> str:
    return f"{count} {one if count == 1 else many}"


def figure(data: dict, mode: str, args: list[str], caption: str | None = None) -> str:
    """The HTML for one board. A caption: line in the Markdown block replaces the default caption."""
    flat = [q for g in data["groups"] for q in g["qs"]]
    before, after = _counts(flat, "before"), _counts(flat, "lamp")
    if mode == "full":
        cap = caption or (
            "My Signal Box answers for this project, read-only. Click a lamp or a checkpoint to read what I recorded. "
            f'The questions are copied from <a href="{GUIDE_URL}">Signal Box in my guide</a> as it stood on 20 October 2026; '
            "use the guide to check your own project.")
        return (f'<figure class="plate wide sbx" aria-labelledby="sbx-cap"><div class="sheet" id="sbx"></div>'
                f'<figcaption id="sbx-cap">{cap}</figcaption></figure>')

    stage = None
    if mode == "checkpoints":
        label = "Unit 2 Signal Box checkpoints"
        legal = sum(q["legal"] for q in flat)
        default = (f"Across {len(flat)} questions, the Unit 2 screen raised {before['o']} concerns and {before['g']} had no "
                   f"concern raised. The ⚖ marks the {legal} legal-trigger questions.")
    elif mode == "stages":
        label = "Unit 2 concern links by project stage"
        links = sum(q["before"] == "o" and s["id"] in q["stages"] for s in data["stages"] for q in flat)
        default = f"The table links {before['o']} Unit 2 concern questions to {links} project-stage assignments."
    elif mode == "before-after":
        label = "Signal Box results before and after the Unit 3 re-test"
        default = (f"The Unit 2 screen raised {before['o']} concerns; {before['g']} had no concern raised. After the Unit 3 "
                   f"re-test, {after['y']} were investigated and recorded, {after['o']} remain open by decision, and "
                   f"{after['g']} had no concern raised.")
    elif mode == "stage":
        stage = args[0]
        if stage not in STAGE_FILES:
            raise ValueError(f"Unknown stage for a Signal Box board: {stage}")
        title = next(s["title"] for s in data["stages"] if s["id"] == stage)
        label = f"{title} Signal Box questions"
        c = _counts([q for q in flat if stage in q["stages"]], "before")
        default = (f"{title}: {_n(c['o'], 'Unit 2 concern', 'Unit 2 concerns')} and "
                   f"{_n(c['g'], 'no-flag question', 'no-flag questions')}. Each row also shows the result after the Unit 3 re-test.")
    else:
        raise ValueError(f"Unknown Signal Box board: {mode}")

    classes = "plate sbx sbm-fig" + (" wide" if "wide" in args else "")
    stage_attr = f' data-stage="{stage}"' if stage else ""
    return (f'<figure class="{classes}"><div class="sheet"><div class="sbm" data-mode="{mode}" role="group" '
            f'aria-label="{html.escape(label, quote=True)}"{stage_attr}></div></div>'
            f"<figcaption>{caption or html.escape(default)}</figcaption></figure>")
