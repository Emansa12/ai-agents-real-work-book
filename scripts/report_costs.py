"""Generate token/cost estimate reports from saved crew artifacts."""

import json
from pathlib import Path

from src.chapters import all_chapter_indices
from src.cost_tracker import ArtifactCostSummary, summarize_artifact_cost

ARTIFACT_DIRS = [
    Path("outputs/research"),
    Path("outputs/drafts"),
    Path("outputs/reviews"),
    Path("latex/generated"),
]
LOGS_DIR = Path("outputs/logs")
REPORT_MD = LOGS_DIR / "cost_report.md"
REPORT_JSON = LOGS_DIR / "cost_report.json"
DEFAULT_MODEL = "gpt-4o-mini"
SKIP_NAMES = {"cost_report.md", "cost_report.json"}


def collect_artifact_paths() -> list[Path]:
    paths: list[Path] = []
    for directory in ARTIFACT_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.iterdir()):
            if not path.is_file() or path.name in SKIP_NAMES:
                continue
            if path.suffix.lower() in {".md", ".tex", ".json"}:
                paths.append(path)
    return paths


def format_markdown_report(summary: ArtifactCostSummary) -> str:
    lines = [
        "# Cost Report (Estimate)",
        "",
        f"- Model: `{summary.model_name}`",
        f"- Files counted: {summary.files_counted}",
        f"- Estimated input tokens: {summary.input_tokens}",
        f"- Estimated output tokens: {summary.output_tokens}",
        f"- Estimated total tokens: {summary.total_tokens}",
        f"- Estimated input cost (USD): ${summary.input_cost_usd:.6f}",
        f"- Estimated output cost (USD): ${summary.output_cost_usd:.6f}",
        f"- Estimated total cost (USD): ${summary.total_cost_usd:.6f}",
        f"- Is estimate: {summary.is_estimate}",
        "",
        "## Notes",
        "",
    ]
    for note in summary.notes:
        lines.append(f"- {note}")
    lines.extend(["", "## Files", ""])
    for file_path in summary.file_paths:
        lines.append(f"- `{file_path}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    paths = collect_artifact_paths()
    summary = summarize_artifact_cost(paths, model_name=DEFAULT_MODEL)

    chapter_count = len(all_chapter_indices())
    if summary.files_counted > 0 and chapter_count > 1:
        projected_all = summary.total_cost_usd * chapter_count
        summary.notes.append(
            f"Rough projected cost for --all ({chapter_count} chapters) "
            f"if each chapter is similar: ${projected_all:.6f} (estimate only)."
        )
        if projected_all >= 1.0:
            summary.notes.append(
                "Budget warning: running --all may exceed $1.00 estimated cost."
            )

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text(format_markdown_report(summary), encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps(summary.model_dump(), indent=2),
        encoding="utf-8",
    )

    print("Cost report generated (estimates only; no live API calls).")
    print(f"Files counted: {summary.files_counted}")
    print(f"Estimated input tokens: {summary.input_tokens}")
    print(f"Estimated output tokens: {summary.output_tokens}")
    print(f"Estimated total tokens: {summary.total_tokens}")
    print(f"Estimated total cost (USD): ${summary.total_cost_usd:.6f}")
    print(f"Markdown report: {REPORT_MD}")
    print(f"JSON report: {REPORT_JSON}")

    for note in summary.notes:
        if "Budget warning" in note:
            print(f"Warning: {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
