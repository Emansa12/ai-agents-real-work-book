"""CrewAI agent factory functions for the book production pipeline."""

from crewai import Agent

from src.agent_config import (
    LATEX_BUILDER_BACKSTORY,
    LATEX_BUILDER_GOAL,
    LATEX_BUILDER_ROLE,
    RESEARCHER_BACKSTORY,
    RESEARCHER_GOAL,
    RESEARCHER_ROLE,
    REVIEWER_BACKSTORY,
    REVIEWER_GOAL,
    REVIEWER_ROLE,
    WRITER_BACKSTORY,
    WRITER_GOAL,
    WRITER_ROLE,
)
from src.config import load_settings
from src.search_adapter import live_internet_search


def _resolve_llm(llm: str | None) -> str:
    if llm is not None:
        return llm
    settings = load_settings()
    return f"openai/{settings.model_name}"


def create_researcher_agent(llm: str | None = None) -> Agent:
    """Create the Researcher Agent with the live internet search tool."""
    return Agent(
        role=RESEARCHER_ROLE,
        goal=RESEARCHER_GOAL,
        backstory=RESEARCHER_BACKSTORY,
        tools=[live_internet_search],
        llm=_resolve_llm(llm),
        verbose=False,
    )


def create_writer_agent(llm: str | None = None) -> Agent:
    """Create the Writer Agent (uses research context in Phase 4 tasks)."""
    return Agent(
        role=WRITER_ROLE,
        goal=WRITER_GOAL,
        backstory=WRITER_BACKSTORY,
        llm=_resolve_llm(llm),
        verbose=False,
    )


def create_reviewer_agent(llm: str | None = None) -> Agent:
    """Create the Reviewer Agent."""
    return Agent(
        role=REVIEWER_ROLE,
        goal=REVIEWER_GOAL,
        backstory=REVIEWER_BACKSTORY,
        llm=_resolve_llm(llm),
        verbose=False,
    )


def create_latex_builder_agent(llm: str | None = None) -> Agent:
    """Create the LaTeX Builder Agent."""
    return Agent(
        role=LATEX_BUILDER_ROLE,
        goal=LATEX_BUILDER_GOAL,
        backstory=LATEX_BUILDER_BACKSTORY,
        llm=_resolve_llm(llm),
        verbose=False,
    )
