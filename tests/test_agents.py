"""Tests for CrewAI agent factories (no live API calls)."""

from crewai import Agent

from src.agent_config import (
    LATEX_BUILDER_ROLE,
    RESEARCHER_ROLE,
    REVIEWER_ROLE,
    WRITER_ROLE,
)
from src.agents import (
    create_latex_builder_agent,
    create_researcher_agent,
    create_reviewer_agent,
    create_writer_agent,
)

TEST_LLM = "openai/gpt-4o-mini"
FORBIDDEN_STATIC_PHRASES = (
    "use static lecture bodies",
    "primary source is the lecture",
    "hardcoded article content",
)


def test_create_researcher_agent_returns_agent() -> None:
    agent = create_researcher_agent(llm=TEST_LLM)

    assert isinstance(agent, Agent)
    assert agent.role == RESEARCHER_ROLE


def test_researcher_mentions_live_search() -> None:
    agent = create_researcher_agent(llm=TEST_LLM)
    combined = f"{agent.goal} {agent.backstory}".lower()

    assert "live" in combined
    assert "search" in combined
    assert agent.tools is not None
    assert len(agent.tools) == 1


def test_create_writer_agent_returns_agent() -> None:
    agent = create_writer_agent(llm=TEST_LLM)

    assert isinstance(agent, Agent)
    assert agent.role == WRITER_ROLE


def test_writer_uses_research_context_not_static_lecture_bodies() -> None:
    agent = create_writer_agent(llm=TEST_LLM)
    combined = f"{agent.goal} {agent.backstory}".lower()

    assert "research" in combined
    for phrase in FORBIDDEN_STATIC_PHRASES:
        assert phrase not in combined


def test_create_reviewer_agent_returns_agent() -> None:
    agent = create_reviewer_agent(llm=TEST_LLM)

    assert isinstance(agent, Agent)
    assert agent.role == REVIEWER_ROLE


def test_reviewer_checks_accuracy_and_citations() -> None:
    agent = create_reviewer_agent(llm=TEST_LLM)
    combined = f"{agent.goal} {agent.backstory}".lower()

    assert "accuracy" in combined
    assert "citation" in combined
    assert "clarity" in combined


def test_create_latex_builder_agent_returns_agent() -> None:
    agent = create_latex_builder_agent(llm=TEST_LLM)

    assert isinstance(agent, Agent)
    assert agent.role == LATEX_BUILDER_ROLE


def test_latex_builder_prepares_latex_fragments() -> None:
    agent = create_latex_builder_agent(llm=TEST_LLM)
    combined = f"{agent.goal} {agent.backstory}".lower()

    assert "latex" in combined
    assert "reviewed" in combined or "review" in combined


def test_latex_builder_requires_xelatex_bidi_safe_output() -> None:
    agent = create_latex_builder_agent(llm=TEST_LLM)
    combined = f"{agent.goal} {agent.backstory}".lower()

    assert "xelatex" in combined
    assert "bidi" in combined or "hebrew" in combined
    assert "begin{hebrew}" in combined or "hebrew environment" in combined
    assert "mixed-direction" in combined or "mixed-direction text" in combined


def test_all_agent_roles_match_expected_names() -> None:
    agents = [
        create_researcher_agent(llm=TEST_LLM),
        create_writer_agent(llm=TEST_LLM),
        create_reviewer_agent(llm=TEST_LLM),
        create_latex_builder_agent(llm=TEST_LLM),
    ]

    roles = {agent.role for agent in agents}
    assert roles == {
        RESEARCHER_ROLE,
        WRITER_ROLE,
        REVIEWER_ROLE,
        LATEX_BUILDER_ROLE,
    }
