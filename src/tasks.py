"""CrewAI task factory functions for the book production pipeline."""

from crewai import Agent, Task

from src.task_config import (
    LATEX_EXPECTED_OUTPUT,
    RESEARCH_EXPECTED_OUTPUT,
    REVIEW_EXPECTED_OUTPUT,
    WRITING_EXPECTED_OUTPUT,
    latex_task_description,
    research_task_description,
    review_task_description,
    writing_task_description,
)

_TOPIC_MARKERS = (
    "chapter topic: ",
    "chapter draft for: ",
    "Review the chapter draft for: ",
    "reviewed chapter content for: ",
)


def create_research_task(agent: Agent, topic_or_chapter: str) -> Task:
    """Create the Research Task requiring live source-backed research."""
    return Task(
        description=research_task_description(topic_or_chapter),
        expected_output=RESEARCH_EXPECTED_OUTPUT,
        agent=agent,
    )


def create_writing_task(agent: Agent, research_task: Task) -> Task:
    """Create the Writing Task that uses research context."""
    topic_or_chapter = _topic_from_task(research_task)
    return Task(
        description=writing_task_description(topic_or_chapter),
        expected_output=WRITING_EXPECTED_OUTPUT,
        agent=agent,
        context=[research_task],
    )


def create_review_task(
    agent: Agent,
    writing_task: Task,
    research_task: Task | None = None,
) -> Task:
    """Create the Review Task with writing and optional research context."""
    topic_or_chapter = _topic_from_task(writing_task)
    context: list[Task] = []
    if research_task is not None:
        context.append(research_task)
    context.append(writing_task)

    return Task(
        description=review_task_description(topic_or_chapter),
        expected_output=REVIEW_EXPECTED_OUTPUT,
        agent=agent,
        context=context,
    )


def create_latex_task(agent: Agent, review_task: Task) -> Task:
    """Create the LaTeX Task that prepares reviewed content for LaTeX output."""
    topic_or_chapter = _topic_from_task(review_task)
    return Task(
        description=latex_task_description(topic_or_chapter),
        expected_output=LATEX_EXPECTED_OUTPUT,
        agent=agent,
        context=[review_task],
    )


def _topic_from_task(task: Task) -> str:
    """Extract chapter topic hint from a task description."""
    description = str(task.description or "")
    for marker in _TOPIC_MARKERS:
        if marker in description:
            segment = description.split(marker, maxsplit=1)[1]
            return segment.split(".", maxsplit=1)[0].strip()
    return "the assigned chapter"
