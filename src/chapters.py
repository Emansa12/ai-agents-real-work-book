"""Planned chapter list for the book (editable)."""

from dataclasses import dataclass

PROJECT_TOPIC = "AI Agents That Replace Real Work: The Future of Automation"


@dataclass(frozen=True)
class Chapter:
    index: int
    title: str


CHAPTERS: list[Chapter] = [
    Chapter(1, "Introduction: When AI Agents Start Doing Real Work"),
    Chapter(2, "What Makes an AI Agent Different from a Chatbot"),
    Chapter(3, "Workflows, Tools, and Real Automation"),
    Chapter(4, "Jobs, Tasks, and Human-in-the-Loop Supervision"),
    Chapter(5, "Risks: Errors, Security, and Responsibility"),
    Chapter(6, "Business Adoption and Future of Work"),
    Chapter(7, "Hebrew-English BiDi Technical Summary"),
    Chapter(8, "Conclusion: The Future of Automation"),
]


def get_chapter_by_index(chapter_number: int) -> Chapter:
    """Return chapter by 1-based index."""
    for chapter in CHAPTERS:
        if chapter.index == chapter_number:
            return chapter
    raise ValueError(
        f"Invalid chapter number {chapter_number}. "
        f"Choose between 1 and {len(CHAPTERS)}."
    )


def all_chapter_indices() -> list[int]:
    return [chapter.index for chapter in CHAPTERS]
