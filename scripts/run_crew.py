"""Run the CrewAI book pipeline for one or more chapters."""

import argparse
import sys

from src.chapters import all_chapter_indices, get_chapter_by_index
from src.crew_runner import run_chapter_crew

LIVE_API_WARNING = "This command uses live OpenAI/Serper API calls."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the CrewAI chapter pipeline with live API research."
    )
    parser.add_argument(
        "--chapter",
        type=int,
        help="Run a specific chapter by number (1-based). Default: chapter 1 only.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all chapters (explicit opt-in; uses many live API calls).",
    )
    return parser


def resolve_chapter_indices(args: argparse.Namespace) -> list[int]:
    if args.all and args.chapter is not None:
        raise ValueError("Use either --chapter or --all, not both.")

    if args.all:
        return all_chapter_indices()

    chapter_number = args.chapter if args.chapter is not None else 1
    get_chapter_by_index(chapter_number)
    return [chapter_number]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        chapter_indices = resolve_chapter_indices(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(LIVE_API_WARNING)

    if args.all:
        print(
            f"Running all {len(chapter_indices)} chapters with live API calls. "
            "This may take significant time and cost."
        )

    for chapter_index in chapter_indices:
        chapter = get_chapter_by_index(chapter_index)
        print(f"Running chapter {chapter.index}: {chapter.title}")
        result = run_chapter_crew(chapter.index, chapter.title)
        print("Artifacts saved:")
        for label, path in result.artifact_paths_written.items():
            print(f"  {label}: {path}")
        for note in result.notes:
            print(f"  note: {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
