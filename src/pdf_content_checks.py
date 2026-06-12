"""Content element PDF verification checks."""

from __future__ import annotations

import re

from src.pdf_check_helpers import read_text, scan_latex_for_secrets
from src.pdf_verification import (
    ASSETS_GRAPH,
    BIDI_TEX,
    DIAGRAMS_TEX,
    FIGURES_TEX,
    FORMULAS_TEX,
    REFERENCES_BIB,
    ROOT,
    TABLES_TEX,
    CheckResult,
)


def content_checks(main_content: str, preamble_content: str) -> list[CheckResult]:
    checks: list[CheckResult] = []

    diagrams_text = read_text(DIAGRAMS_TEX).lower() if DIAGRAMS_TEX.is_file() else ""
    diagrams_ok = DIAGRAMS_TEX.is_file() and "tikzpicture" in diagrams_text
    checks.append(
        CheckResult(
            "TikZ diagram",
            diagrams_ok and "diagrams.tex" in main_content,
            "diagrams.tex with tikzpicture",
        )
    )

    figures_content = read_text(FIGURES_TEX) if FIGURES_TEX.is_file() else ""
    graph_ok = (
        FIGURES_TEX.is_file()
        and "automation_impact_graph" in figures_content
        and "includegraphics" in figures_content
        and ASSETS_GRAPH.is_file()
        and ASSETS_GRAPH.stat().st_size > 0
    )
    checks.append(
        CheckResult(
            "Python-generated graph",
            graph_ok,
            f"figures.tex + {ASSETS_GRAPH.relative_to(ROOT)}",
        )
    )

    tables_content = read_text(TABLES_TEX) if TABLES_TEX.is_file() else ""
    checks.append(
        CheckResult(
            "table",
            TABLES_TEX.is_file()
            and "tabularx" in tables_content
            and "\\toprule" in tables_content,
            "tables.tex with tabularx/booktabs",
        )
    )

    formulas_content = read_text(FORMULAS_TEX) if FORMULAS_TEX.is_file() else ""
    checks.append(
        CheckResult(
            "highlighted formula",
            FORMULAS_TEX.is_file() and "formulabox" in formulas_content,
            "formulas.tex with formulabox",
        )
    )

    bidi_content = read_text(BIDI_TEX) if BIDI_TEX.is_file() else ""
    checks.append(
        CheckResult(
            "Hebrew-English BiDi section",
            BIDI_TEX.is_file()
            and re.search(r"[\u0590-\u05FF]", bidi_content) is not None
            and "hebrew" in bidi_content.lower()
            and "bidi_section.tex" in main_content,
            "bidi_section.tex with Hebrew text",
        )
    )

    cite_count = len(re.findall(r"\\cite\{", main_content))
    for extra in (DIAGRAMS_TEX, FIGURES_TEX, TABLES_TEX, FORMULAS_TEX, BIDI_TEX):
        if extra.is_file():
            cite_count += len(re.findall(r"\\cite\{", read_text(extra)))
    checks.append(
        CheckResult(
            "citations",
            cite_count > 0,
            f"{cite_count} \\cite command(s) in LaTeX sources",
        )
    )

    checks.append(
        CheckResult(
            "bibliography",
            "\\printbibliography" in main_content and REFERENCES_BIB.is_file(),
            "printbibliography + references.bib",
        )
    )

    styled_boxes = all(
        token in preamble_content
        for token in ("insightbox", "warningbox", "formulabox", "chapterintrobox")
    )
    checks.append(
        CheckResult(
            "callout/styled boxes",
            styled_boxes,
            "insightbox, warningbox, formulabox, chapterintrobox in preamble",
        )
    )

    secret_hits = scan_latex_for_secrets()
    checks.append(
        CheckResult(
            "no API keys or secrets",
            len(secret_hits) == 0,
            "no secret patterns in latex/*.tex"
            if not secret_hits
            else "; ".join(secret_hits),
        )
    )

    return checks
