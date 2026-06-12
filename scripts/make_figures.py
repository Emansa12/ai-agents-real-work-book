"""Generate deterministic matplotlib figures for the LaTeX book (no API keys)."""

from pathlib import Path

import matplotlib.pyplot as plt

ASSETS_DIR = Path("assets")
OUTPUT_PATH = ASSETS_DIR / "automation_impact_graph.png"

# Deterministic data: workflow maturity vs automation impact / supervision.
CATEGORIES = [
    "Routine Admin",
    "Structured Workflows",
    "Multi-step Tasks",
    "Complex Judgment",
]
AUTOMATION_IMPACT = [84, 71, 47, 21]
HUMAN_SUPERVISION = [16, 29, 53, 79]

# Palette aligned with latex/preamble.tex
COLOR_NAVY = "#185294"
COLOR_BLUE = "#3282B2"
COLOR_ORANGE = "#D6602C"


def build_automation_impact_graph() -> Path:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    x = range(len(CATEGORIES))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        AUTOMATION_IMPACT,
        width,
        label="Automation impact (%)",
        color=COLOR_BLUE,
    )
    ax.bar(
        [i + width / 2 for i in x],
        HUMAN_SUPERVISION,
        width,
        label="Human supervision needed (%)",
        color=COLOR_ORANGE,
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(CATEGORIES, rotation=12, ha="right")
    ax.set_ylabel("Percent")
    ax.set_title("AI Agent Automation Impact vs Human Supervision")
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)

    return OUTPUT_PATH


def main() -> int:
    path = build_automation_impact_graph()
    print(f"Saved figure: {path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
