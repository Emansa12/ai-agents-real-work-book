"""PDF artifact and build configuration checks."""

from src.pdf_check_helpers import pdf_page_count, pdf_tracked_by_git, read_text
from src.pdf_verification import (
    BUILD_SCRIPT,
    MAIN_PDF,
    MAIN_TEX,
    MAX_PAGES,
    MIN_PAGES,
    PREAMBLE_TEX,
    ROOT,
    CheckResult,
)


def load_main_sources() -> tuple[str, str]:
    main_content = read_text(MAIN_TEX) if MAIN_TEX.is_file() else ""
    preamble_content = read_text(PREAMBLE_TEX) if PREAMBLE_TEX.is_file() else ""
    return main_content, preamble_content


def artifact_checks(main_content: str) -> list[CheckResult]:
    pdf_tracked = pdf_tracked_by_git()
    page_count = pdf_page_count(MAIN_PDF)
    page_ok = page_count is not None and MIN_PAGES <= page_count <= MAX_PAGES
    xelatex_configured = "xelatex" in read_text(BUILD_SCRIPT).lower()

    return [
        CheckResult(
            "PDF not tracked by git",
            not pdf_tracked,
            "latex/main.pdf is gitignored (not tracked)"
            if not pdf_tracked
            else "latex/main.pdf is tracked by git",
        ),
        CheckResult(
            "PDF exists",
            MAIN_PDF.is_file() and MAIN_PDF.stat().st_size > 0,
            str(MAIN_PDF.relative_to(ROOT)),
        ),
        CheckResult(
            "page count valid",
            page_ok,
            f"{page_count} pages (expected {MIN_PAGES}-{MAX_PAGES})"
            if page_count is not None
            else "PDF page count unavailable (install pymupdf or build PDF)",
        ),
        CheckResult(
            "XeLaTeX build configured",
            xelatex_configured and "% !TeX program = xelatex" in main_content,
            "build_pdf.py and main.tex use XeLaTeX",
        ),
    ]
