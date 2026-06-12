"""Factory for the sequential book production crew (definition only; no kickoff)."""

from crewai import Crew, Process

from src.agents import (
    create_latex_builder_agent,
    create_researcher_agent,
    create_reviewer_agent,
    create_writer_agent,
)
from src.tasks import (
    create_latex_task,
    create_research_task,
    create_review_task,
    create_writing_task,
)


def create_book_crew(topic_or_chapter: str, llm: str | None = None) -> Crew:
    """
    Build a sequential crew for one chapter topic.

    Creates agents and tasks but does not run kickoff.
    """
    researcher = create_researcher_agent(llm=llm)
    writer = create_writer_agent(llm=llm)
    reviewer = create_reviewer_agent(llm=llm)
    latex_builder = create_latex_builder_agent(llm=llm)

    research_task = create_research_task(researcher, topic_or_chapter)
    writing_task = create_writing_task(writer, research_task)
    review_task = create_review_task(reviewer, writing_task, research_task)
    latex_task = create_latex_task(latex_builder, review_task)

    return Crew(
        agents=[researcher, writer, reviewer, latex_builder],
        tasks=[research_task, writing_task, review_task, latex_task],
        process=Process.sequential,
        verbose=False,
    )
