"""Execute one chapter crew run and persist artifacts."""

from dataclasses import dataclass, field
from typing import Any

from crewai import Task

from src.config import load_settings
from src.crew_factory import create_book_crew
from src.run_artifacts import artifact_paths, save_run_metadata, save_text_artifact


@dataclass
class ChapterRunResult:
    chapter_index: int
    chapter_title: str
    kickoff_result: str
    artifact_paths_written: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def run_chapter_crew(chapter_index: int, chapter_title: str) -> ChapterRunResult:
    """Run the full crew pipeline for one chapter and save artifacts."""
    settings = load_settings()
    secrets = [settings.openai_api_key, settings.serper_api_key]

    crew = create_book_crew(chapter_title)
    kickoff_output = crew.kickoff()
    kickoff_text = _extract_kickoff_text(kickoff_output)

    paths = artifact_paths(chapter_index)
    written: dict[str, str] = {}
    notes: list[str] = []

    task_outputs = _collect_task_outputs(crew.tasks)
    if len(task_outputs) == 4:
        save_text_artifact(paths["research"], task_outputs[0], secrets=secrets)
        save_text_artifact(paths["draft"], task_outputs[1], secrets=secrets)
        save_text_artifact(paths["review"], task_outputs[2], secrets=secrets)
        save_text_artifact(paths["latex"], task_outputs[3], secrets=secrets)
        written = {
            "research": str(paths["research"]),
            "draft": str(paths["draft"]),
            "review": str(paths["review"]),
            "latex": str(paths["latex"]),
        }
    else:
        notes.append(
            "Per-task outputs were not all available; "
            "saved combined kickoff result only."
        )
        save_text_artifact(paths["combined"], kickoff_text, secrets=secrets)
        written["combined"] = str(paths["combined"])

    log_path = save_run_metadata(
        chapter_index=chapter_index,
        chapter_title=chapter_title,
        artifact_paths_written=written,
        notes=notes,
        secrets=secrets,
    )
    written["log"] = str(log_path)

    return ChapterRunResult(
        chapter_index=chapter_index,
        chapter_title=chapter_title,
        kickoff_result=kickoff_text,
        artifact_paths_written=written,
        notes=notes,
    )


def _extract_kickoff_text(kickoff_output: Any) -> str:
    if kickoff_output is None:
        return ""
    raw = getattr(kickoff_output, "raw", kickoff_output)
    return str(raw)


def _collect_task_outputs(tasks: list[Task]) -> list[str]:
    outputs: list[str] = []
    for task in tasks:
        text = _extract_task_output(task)
        if text is None:
            return []
        outputs.append(text)
    return outputs


def _extract_task_output(task: Task) -> str | None:
    output = task.output
    if output is None:
        return None
    raw = getattr(output, "raw", output)
    text = str(raw).strip()
    if not text:
        return None
    return text
