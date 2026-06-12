"""Tests for CrewAI task factories (no live API calls)."""

from crewai import Task

from src.agents import (
    create_latex_builder_agent,
    create_researcher_agent,
    create_reviewer_agent,
    create_writer_agent,
)
from src.task_config import PROJECT_TOPIC
from src.tasks import (
    create_latex_task,
    create_research_task,
    create_review_task,
    create_writing_task,
)

TEST_LLM = "openai/gpt-4o-mini"
CHAPTER_TOPIC = "How AI agents automate office workflows"
FORBIDDEN_STATIC_PHRASES = (
    "use static lecture bodies",
    "primary source is the lecture",
    "hardcoded article content",
)


def test_create_research_task() -> None:
    agent = create_researcher_agent(llm=TEST_LLM)
    task = create_research_task(agent, CHAPTER_TOPIC)

    assert isinstance(task, Task)
    assert CHAPTER_TOPIC in task.description
    assert PROJECT_TOPIC in task.description
    assert "live" in task.description.lower()
    assert task.expected_output is not None


def test_create_writing_task_uses_research_context() -> None:
    researcher = create_researcher_agent(llm=TEST_LLM)
    writer = create_writer_agent(llm=TEST_LLM)
    research_task = create_research_task(researcher, CHAPTER_TOPIC)
    writing_task = create_writing_task(writer, research_task)

    assert isinstance(writing_task, Task)
    assert writing_task.context is not None
    assert research_task in writing_task.context
    combined = f"{writing_task.description} {writing_task.expected_output}".lower()
    assert "research" in combined
    for phrase in FORBIDDEN_STATIC_PHRASES:
        assert phrase not in combined


def test_create_review_task_uses_context() -> None:
    researcher = create_researcher_agent(llm=TEST_LLM)
    writer = create_writer_agent(llm=TEST_LLM)
    reviewer = create_reviewer_agent(llm=TEST_LLM)
    research_task = create_research_task(researcher, CHAPTER_TOPIC)
    writing_task = create_writing_task(writer, research_task)
    review_task = create_review_task(reviewer, writing_task, research_task)

    assert isinstance(review_task, Task)
    assert review_task.context is not None
    assert writing_task in review_task.context
    assert research_task in review_task.context
    combined = review_task.description.lower()
    assert "accuracy" in combined
    assert "citation" in combined
    assert "clarity" in combined


def test_create_latex_task_uses_review_context() -> None:
    researcher = create_researcher_agent(llm=TEST_LLM)
    writer = create_writer_agent(llm=TEST_LLM)
    reviewer = create_reviewer_agent(llm=TEST_LLM)
    latex_builder = create_latex_builder_agent(llm=TEST_LLM)
    research_task = create_research_task(researcher, CHAPTER_TOPIC)
    writing_task = create_writing_task(writer, research_task)
    review_task = create_review_task(reviewer, writing_task, research_task)
    latex_task = create_latex_task(latex_builder, review_task)

    assert isinstance(latex_task, Task)
    assert latex_task.context is not None
    assert review_task in latex_task.context
    combined = f"{latex_task.description} {latex_task.expected_output}".lower()
    assert "latex" in combined
