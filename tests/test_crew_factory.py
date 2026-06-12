"""Tests for book crew factory (no kickoff, no live API calls)."""

from crewai import Crew, Process

from src.crew_factory import create_book_crew

TEST_LLM = "openai/gpt-4o-mini"
CHAPTER_TOPIC = "Autonomous agents in customer support"


def test_create_book_crew_returns_crew() -> None:
    crew = create_book_crew(CHAPTER_TOPIC, llm=TEST_LLM)

    assert isinstance(crew, Crew)


def test_create_book_crew_has_four_agents_and_tasks() -> None:
    crew = create_book_crew(CHAPTER_TOPIC, llm=TEST_LLM)

    assert len(crew.agents) == 4
    assert len(crew.tasks) == 4


def test_create_book_crew_uses_sequential_process() -> None:
    crew = create_book_crew(CHAPTER_TOPIC, llm=TEST_LLM)

    assert crew.process == Process.sequential


def test_create_book_crew_topic_in_research_task() -> None:
    crew = create_book_crew(CHAPTER_TOPIC, llm=TEST_LLM)
    research_task = crew.tasks[0]

    assert CHAPTER_TOPIC in research_task.description
