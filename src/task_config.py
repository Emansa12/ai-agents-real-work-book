"""Task descriptions and expected outputs for the CrewAI workflow."""

from src.agent_config import PROJECT_TOPIC

RESEARCH_EXPECTED_OUTPUT = (
    "Structured research notes with live source titles, URLs, snippets, "
    "dates when available, and short summaries tied to each source."
)

WRITING_EXPECTED_OUTPUT = (
    "A chapter draft written from the research notes only, with inline "
    "citation placeholders referencing the live sources."
)

REVIEW_EXPECTED_OUTPUT = (
    "An editorial review covering accuracy, clarity, citation quality, "
    "topic alignment, and a list of required fixes."
)

LATEX_EXPECTED_OUTPUT = (
    "LaTeX-ready chapter fragments with safe escaping, preserved citations, "
    "and section headings suitable for latex/generated/. "
    "XeLaTeX-compatible output only: use preamble BiDi macros for Hebrew, "
    "keep English terms out of Hebrew paragraphs, and avoid fragile "
    "mixed-direction text."
)


def research_task_description(topic_or_chapter: str) -> str:
    return (
        f"Research live internet sources for the chapter topic: {topic_or_chapter}. "
        f"The book topic is {PROJECT_TOPIC}. "
        "Use the live internet search tool to find current sources. "
        "Do not use offline caches, fake data, or static lecture bodies. "
        "Summarize findings with titles, URLs, snippets, and dates when available."
    )


def writing_task_description(topic_or_chapter: str) -> str:
    return (
        f"Write a chapter draft for: {topic_or_chapter}. "
        f"Use only the research notes from the Research Task as your source material. "
        f"Stay aligned with {PROJECT_TOPIC}. "
        "Do not copy course PDFs, lecture slides, or prewritten book text."
    )


def review_task_description(topic_or_chapter: str) -> str:
    return (
        f"Review the chapter draft for: {topic_or_chapter}. "
        "Check accuracy against the research notes, clarity of prose, "
        "citation quality, and alignment with "
        f"{PROJECT_TOPIC}. "
        "Flag unsupported claims and missing references."
    )


def latex_task_description(topic_or_chapter: str) -> str:
    return (
        f"Convert the reviewed chapter content for: {topic_or_chapter} "
        "into LaTeX-ready fragments. Preserve meaning, citations, and structure. "
        "Apply safe LaTeX escaping for special characters. "
        "The PDF builds with XeLaTeX and polyglossia BiDi: use Hebrew "
        "environments from latex/preamble.tex "
        "(\\begin{hebrew}, \\texthebrew{}, flushright blocks). "
        "Do not embed English workflow terms inside Hebrew paragraphs. "
        "Put English terms in English prose, definition lists, or tables only. "
        "Do not output fragile raw mixed-direction text or makebox alignment hacks."
    )
