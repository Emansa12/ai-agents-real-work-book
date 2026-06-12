"""Structure-related PDF verification checks."""

from src.pdf_verification import CheckResult


def structure_checks(main_content: str, preamble_content: str) -> list[CheckResult]:
    chapter_count = main_content.count(r"\chapter{")
    return [
        CheckResult(
            "cover page",
            "\\begin{titlepage}" in main_content and "\\booktitle" in main_content,
            "titlepage with book title",
        ),
        CheckResult(
            "table of contents",
            "\\tableofcontents" in main_content,
            "\\tableofcontents in main.tex",
        ),
        CheckResult(
            "headers/footers",
            "\\pagestyle{fancy}" in main_content and "fancyhdr" in preamble_content,
            "fancy page style enabled",
        ),
        CheckResult(
            "chapters",
            chapter_count >= 5,
            f"{chapter_count} chapter(s) in main.tex",
        ),
    ]
