"""Tests for LaTeX book structure (no LaTeX installation required)."""

from pathlib import Path

LATEX_DIR = Path("latex")
MAIN_TEX = LATEX_DIR / "main.tex"
PREAMBLE_TEX = LATEX_DIR / "preamble.tex"
REFERENCES_BIB = LATEX_DIR / "references.bib"
BUILD_SCRIPT = Path("scripts/build_pdf.py")


def test_main_tex_exists() -> None:
    assert MAIN_TEX.is_file()


def test_preamble_tex_exists() -> None:
    assert PREAMBLE_TEX.is_file()


def test_main_tex_references_preamble() -> None:
    content = MAIN_TEX.read_text(encoding="utf-8")
    assert "preamble.tex" in content


def test_main_tex_has_table_of_contents() -> None:
    content = MAIN_TEX.read_text(encoding="utf-8")
    assert "\\tableofcontents" in content


def test_main_tex_includes_generated_chapter_fragments() -> None:
    content = MAIN_TEX.read_text(encoding="utf-8")
    assert "chapter_01" in content
    assert "generated" in content


def test_preamble_has_bidi_and_xelatex_support() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    lowered = content.lower()
    assert "fontspec" in lowered
    assert "polyglossia" in lowered or "babel" in lowered
    assert "hebrew" in lowered
    assert "xelatex" in lowered or "fontspec" in lowered


def test_preamble_includes_tikz() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    assert "tikz" in content.lower()


def test_preamble_includes_tcolorbox() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    assert "tcolorbox" in content
    assert "insightbox" in content
    assert "warningbox" in content
    assert "formulabox" in content


def test_preamble_includes_fancyhdr() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    assert "fancyhdr" in content


def test_preamble_includes_styled_headings() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    assert "titlesec" in content


def test_preamble_has_bibliography_setup() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    assert "biblatex" in content
    assert "references.bib" in content


def test_preamble_has_professional_color_palette() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    assert "titleNavy" in content
    assert "boxBg" in content
    assert "accentOrange" in content or "warningAccent" in content


def test_preamble_has_chapter_banner_macro() -> None:
    content = PREAMBLE_TEX.read_text(encoding="utf-8")
    assert "chapterbanner" in content


def test_build_script_exists() -> None:
    assert BUILD_SCRIPT.is_file()


def test_build_script_has_xelatex_fallback() -> None:
    content = BUILD_SCRIPT.read_text(encoding="utf-8")
    assert "run_direct_xelatex_build" in content
    assert "xelatex" in content
    assert "biber" in content


def test_references_bib_exists() -> None:
    assert REFERENCES_BIB.is_file()


def test_references_bib_has_live_research_entries() -> None:
    content = REFERENCES_BIB.read_text(encoding="utf-8")
    assert "arxiv2506workagents" in content
    assert "mediumworkflowagents" in content


def test_main_tex_does_not_cite_placeholder_bibliography() -> None:
    content = MAIN_TEX.read_text(encoding="utf-8")
    assert "placeholderphase8" not in content


def test_build_script_sanitizes_markdown_fences() -> None:
    from scripts.build_pdf import sanitize_tex_fragment

    raw = "```latex\n\\section{Test}\n```\n"
    cleaned = sanitize_tex_fragment(raw)
    assert "```" not in cleaned
    assert "\\section{Test}" in cleaned
