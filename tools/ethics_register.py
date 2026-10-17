"""Build figures and a text summary from the Unit 2 ethics screen CSV."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch


SITE = Path(__file__).resolve().parent.parent
PROJECT = Path(os.environ.get(
    "HLE_PROJECT",
    str(SITE.parent / "Code-Institute-DA-with-AI-Unit-3-Assessment"),
))
SCREEN_CSV = PROJECT / "data" / "ethics" / "unit2_screen_results.csv"
OUT = SITE / "assets" / "img" / "second-look"

FIELDS = [
    "q", "checkpoint", "checkpoint_name", "question_short", "legal_trigger",
    "lamp", "severity", "stages", "evidence", "action", "plan_ref", "status",
]
CHECKPOINTS = {
    "A": "Purpose and benefit",
    "B": "Data",
    "C": "Decisions and oversight",
    "D": "People affected",
    "E": "Safety and robustness",
    "F": "Responsibility and law",
}
STAGE_NAMES = {
    "S1": "Choosing sources",
    "S2": "Preparing and aggregating",
    "S3": "Joined table",
    "S4": "Hypothesis test",
    "S5": "Machine learning",
    "S6": "Hotspots",
    "S7": "Dashboards and site",
}
LEGAL_QUESTIONS = {5, 6, 12, 26}

# The neutral colours follow assets/site.css. Orange and grey distinguish the
# screen lamps; the marker shape also carries the meaning.
PAPER = "#eceee8"
INK = "#18262e"
MUTED = "#4b5b62"
RULE = "#c9cfc6"
TEAL = "#1d5c63"
ORANGE = "#b94f13"
NO_FLAG = "#7a878c"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": INK,
    "axes.labelcolor": INK,
    "svg.fonttype": "none",
})


def load_records(path: Path = SCREEN_CSV) -> list[dict[str, str]]:
    """Read the source CSV and enforce the report's published totals."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"Unexpected CSV columns: {reader.fieldnames}")
        records = list(reader)

    if len(records) != 27:
        raise ValueError(f"Expected 27 questions, found {len(records)}")
    for record in records:
        record["q"] = int(record["q"])
        if record["checkpoint"] not in CHECKPOINTS:
            raise ValueError(f"Unexpected checkpoint for Q{record['q']}")
        if record["checkpoint_name"] != CHECKPOINTS[record["checkpoint"]]:
            raise ValueError(f"Checkpoint name mismatch for Q{record['q']}")
        if record["lamp"] not in {"concern", "no_flag"}:
            raise ValueError(f"Unexpected lamp for Q{record['q']}")
        if record["legal_trigger"] not in {"true", "false"}:
            raise ValueError(f"Unexpected legal_trigger for Q{record['q']}")

    records.sort(key=lambda record: record["q"])
    if [record["q"] for record in records] != list(range(1, 28)):
        raise ValueError("Question numbers must be unique and run from 1 to 27")

    concerns = [record for record in records if record["lamp"] == "concern"]
    no_flags = [record for record in records if record["lamp"] == "no_flag"]
    legal = [record for record in records if record["legal_trigger"] == "true"]
    assert len(concerns) == 17, f"Expected 17 concerns, found {len(concerns)}"
    assert len(no_flags) == 10, f"Expected 10 no-flags, found {len(no_flags)}"
    assert len(legal) == 4, f"Expected 4 legal triggers, found {len(legal)}"
    assert {record["q"] for record in legal} == LEGAL_QUESTIONS
    assert all(record["lamp"] == "no_flag" for record in legal)
    return records


def write_screen_summary(records: list[dict[str, str]]) -> Path:
    lines = [
        "# Ethics screen summary",
        "",
        "A yes is a concern to investigate, not a finding of harm. A no-flag means no concern was raised; it does not mean safe.",
        "",
        "| Question | Checkpoint | Short question | Lamp | Stages |",
        "|---:|---|---|---|---|",
    ]
    for row in records:
        lamp = "🟠 concern" if row["lamp"] == "concern" else "⚪ no flag"
        question = row["question_short"].replace("|", "\\|")
        checkpoint = f"{row['checkpoint']} · {row['checkpoint_name']}"
        lines.append(
            f"| Q{row['q']} | {checkpoint} | {question} | {lamp} | {row['stages']} |"
        )
    path = OUT / "screen-summary.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def save_lamp_board(records: list[dict[str, str]]) -> Path:
    grouped = {
        checkpoint: [record for record in records if record["checkpoint"] == checkpoint]
        for checkpoint in CHECKPOINTS
    }
    fig, ax = plt.subplots(figsize=(7, 6.5), dpi=96)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.text(0.25, 6.72, "Screen lamps by checkpoint", fontsize=16, weight="bold", va="top")
    ax.text(
        0.25, 6.3,
        "Question numbers and filled or hollow markers repeat the colour meaning.",
        fontsize=9.5, color=MUTED, va="top",
    )

    y_positions = [5.65, 4.8, 3.95, 3.1, 2.25, 1.4]
    for (checkpoint, name), y in zip(CHECKPOINTS.items(), y_positions):
        short_name = name.replace(" and ", " & ")
        if checkpoint == "F":
            short_name = "Responsibility & law"
        ax.text(0.28, y, f"{checkpoint} · {short_name}", fontsize=10.2, weight="bold", va="center")
        ax.plot([0.28, 9.55], [y - 0.39, y - 0.39], color=RULE, linewidth=0.8)
        for index, row in enumerate(grouped[checkpoint]):
            x = 4.65 + index * 0.78
            concern = row["lamp"] == "concern"
            edge = ORANGE if concern else NO_FLAG
            face = ORANGE if concern else PAPER
            ax.add_patch(Circle((x, y), 0.24, edgecolor=edge, facecolor=face, linewidth=1.8))
            ax.text(
                x, y, str(row["q"]), ha="center", va="center", fontsize=8.5,
                weight="bold", color=PAPER if concern else INK,
            )
            if row["legal_trigger"] == "true":
                ax.text(x + 0.18, y + 0.21, "⚖", color=TEAL, fontsize=10, ha="left", va="bottom")

    ax.add_patch(Circle((0.52, 0.56), 0.14, edgecolor=ORANGE, facecolor=ORANGE, linewidth=1.5))
    ax.text(0.8, 0.56, "Concern", va="center", fontsize=9.5)
    ax.add_patch(Circle((2.35, 0.56), 0.14, edgecolor=NO_FLAG, facecolor=PAPER, linewidth=1.5))
    ax.text(2.63, 0.56, "No flag", va="center", fontsize=9.5)
    ax.text(4.15, 0.56, "⚖  Legal-trigger question", va="center", fontsize=9.5, color=TEAL)

    path = OUT / "lamp-board.svg"
    fig.savefig(path, format="svg", bbox_inches="tight", facecolor=PAPER,
                metadata={"Title": "Ethics screen lamps by checkpoint"})
    plt.close(fig)
    return path


def save_stage_grid(records: list[dict[str, str]]) -> Path:
    concerns = [record for record in records if record["lamp"] == "concern"]
    stage_ids = list(STAGE_NAMES)
    fig, ax = plt.subplots(figsize=(11.2, 5.8), dpi=96)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(-0.8, len(concerns) + 1.65)
    ax.set_ylim(-0.85, len(stage_ids) - 0.35)
    ax.set_aspect("equal", adjustable="box")
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.set_xticks(range(len(concerns)))
    ax.set_xticklabels([f"Q{row['q']}" for row in concerns], fontsize=8.5)
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", length=0, pad=5)
    ax.set_yticks(range(len(stage_ids)))
    ax.set_yticklabels(stage_ids, fontsize=9.5, weight="bold")
    ax.tick_params(axis="y", length=0, pad=7)
    ax.grid(axis="y", color=RULE, linewidth=0.8)
    ax.spines[:].set_visible(False)
    ax.set_title("Concern links across the seven stages", loc="left", fontsize=13, weight="bold", pad=18)

    row_totals = []
    for y, stage in enumerate(stage_ids):
        total = 0
        for x, row in enumerate(concerns):
            if stage in row["stages"].split(";"):
                ax.add_patch(Circle((x, y), 0.16, facecolor=ORANGE, edgecolor=ORANGE, linewidth=1))
                total += 1
        row_totals.append(total)
        ax.text(len(concerns) + 0.4, y, str(total), va="center", ha="center", fontsize=9.5, weight="bold")

    ax.text(len(concerns) + 0.4, -0.62, "Total", va="center", ha="center", fontsize=8, color=MUTED)
    path = OUT / "stage-grid.svg"
    fig.savefig(path, format="svg", bbox_inches="tight", facecolor=PAPER,
                metadata={"Title": "Ethics concerns by project stage"})
    plt.close(fig)
    return path


def save_checkpoint_flow(records: list[dict[str, str]]) -> Path:
    counts = {
        checkpoint: sum(
            row["checkpoint"] == checkpoint and row["lamp"] == "concern"
            for row in records
        )
        for checkpoint in CHECKPOINTS
    }
    fig, ax = plt.subplots(figsize=(5.2, 2.65), dpi=96)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 7.35)
    ax.set_ylim(0, 3)
    ax.axis("off")
    ax.text(0.08, 2.78, "Six checkpoints · concern count below each letter", fontsize=12.2,
            weight="bold", va="top")

    positions = [0.42 + index * 0.74 for index in range(6)]
    y = 1.75
    for index, (checkpoint, x) in enumerate(zip(CHECKPOINTS, positions)):
        ax.add_patch(Circle((x, y), 0.25, facecolor=TEAL, edgecolor=TEAL, linewidth=1.2))
        ax.text(x, y, checkpoint, ha="center", va="center", color=PAPER, fontsize=11, weight="bold")
        ax.text(x, 1.12, str(counts[checkpoint]), ha="center", va="center", fontsize=10.5, weight="bold")
        if index < len(positions) - 1:
            ax.annotate("", xy=(positions[index + 1] - 0.28, y), xytext=(x + 0.28, y),
                        arrowprops={"arrowstyle": "->", "color": MUTED, "linewidth": 1.3})

    box = FancyBboxPatch(
        (4.9, 0.63), 2.28, 1.84,
        boxstyle="round,pad=0.14,rounding_size=0.12",
        facecolor="#e1e5dd", edgecolor=TEAL, linewidth=1.25,
    )
    ax.add_patch(box)
    ax.annotate("", xy=(4.84, y), xytext=(positions[-1] + 0.28, y),
                arrowprops={"arrowstyle": "->", "color": MUTED, "linewidth": 1.3})
    ax.text(6.04, 2.08, "Owner decides", ha="center", va="center", fontsize=10, weight="bold")
    ax.text(6.04, 1.48, "proceed · narrow\nredesign · stop", ha="center", va="center", fontsize=9.2)
    ax.text(0.42, 0.53, "Concern count", fontsize=8.5, color=MUTED, ha="left", va="center")

    path = OUT / "checkpoint-flow.svg"
    fig.savefig(path, format="svg", bbox_inches="tight", facecolor=PAPER,
                metadata={"Title": "Ethics screen checkpoint flow"})
    plt.close(fig)
    return path


def main() -> None:
    records = load_records()
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = [
        save_lamp_board(records),
        save_stage_grid(records),
        save_checkpoint_flow(records),
        write_screen_summary(records),
    ]
    print("Loaded 27 questions: 17 concerns, 10 no-flags, 4 legal triggers (all no-flag).")
    for path in outputs:
        print(f"Wrote {path.relative_to(SITE)}")


if __name__ == "__main__":
    main()
