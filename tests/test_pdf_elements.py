"""Tests for Phase 8 required PDF elements (no LaTeX installation required)."""

import re
from pathlib import Path

MAKE_FIGURES = Path("scripts/make_figures.py")
ASSETS_GRAPH = Path("assets/automation_impact_graph.png")
MAIN_TEX = Path("latex/main.tex")
DIAGRAMS_TEX = Path("latex/diagrams.tex")
FIGURES_TEX = Path("latex/figures.tex")
TABLES_TEX = Path("latex/tables.tex")
FORMULAS_TEX = Path("latex/formulas.tex")
BIDI_TEX = Path("latex/bidi_section.tex")
REFERENCES_BIB = Path("latex/references.bib")


def test_make_figures_script_exists() -> None:
    assert MAKE_FIGURES.is_file()


def test_make_figures_defines_assets_graph_path() -> None:
    content = MAKE_FIGURES.read_text(encoding="utf-8")
    assert "automation_impact_graph.png" in content
    assert "assets" in content


def test_main_tex_includes_required_element_files() -> None:
    content = MAIN_TEX.read_text(encoding="utf-8")
    fragments = (
        "diagrams.tex",
        "figures.tex",
        "tables.tex",
        "formulas.tex",
        "bidi_section.tex",
    )
    for fragment in fragments:
        assert fragment in content


def test_diagrams_tex_contains_tikz() -> None:
    content = DIAGRAMS_TEX.read_text(encoding="utf-8")
    assert "tikzpicture" in content.lower()
    assert "From Human Task to Agentic Workflow" in content
    assert "AI Agent" in content and "Tools" in content
    assert "LaTeX" not in content
    assert "Researcher Agent" not in content


def test_tables_tex_uses_booktabs_and_tabularx() -> None:
    content = TABLES_TEX.read_text(encoding="utf-8")
    assert "tabularx" in content
    assert "\\toprule" in content
    assert "\\bottomrule" in content


def test_formulas_tex_contains_formulabox() -> None:
    content = FORMULAS_TEX.read_text(encoding="utf-8")
    assert "formulabox" in content
    assert "V_" in content or "eta_" in content


def test_bidi_section_has_hebrew_and_technical_terms() -> None:
    content = BIDI_TEX.read_text(encoding="utf-8")
    assert re.search(r"[\u0590-\u05FF]", content)
    for term in ("Agent", "Task", "Workflow", "Tool", "API Key", "Human-in-the-loop"):
        assert term in content
    assert "hebrew" in content.lower()
    assert "סוכני בינה מלאכותית יכולים לבצע משימות מוגדרות" in content
    assert "Mixed-language example" in content


def test_figures_tex_references_python_graph() -> None:
    content = FIGURES_TEX.read_text(encoding="utf-8")
    assert "automation_impact_graph" in content
    assert "includegraphics" in content


def _collect_cite_keys(path: Path) -> list[str]:
    return re.findall(r"\\cite\{([^}]+)\}", path.read_text(encoding="utf-8"))


def test_references_bib_has_cited_entries() -> None:
    bib = REFERENCES_BIB.read_text(encoding="utf-8")
    cited_keys: list[str] = []
    for tex_path in (
        MAIN_TEX,
        DIAGRAMS_TEX,
        FIGURES_TEX,
        TABLES_TEX,
        FORMULAS_TEX,
        BIDI_TEX,
    ):
        cited_keys.extend(_collect_cite_keys(tex_path))

    all_keys: set[str] = set()
    for group in cited_keys:
        for key in group.split(","):
            all_keys.add(key.strip())

    for key in all_keys:
        assert key in bib

    assert "placeholderphase8" not in bib


def test_no_placeholderphase8_citation_in_latex_source() -> None:
    latex_dir = Path("latex")
    for path in latex_dir.glob("*.tex"):
        assert "placeholderphase8" not in path.read_text(encoding="utf-8")


def test_make_figures_generates_graph(tmp_path: Path) -> None:
    import scripts.make_figures as mf
    from scripts.make_figures import build_automation_impact_graph

    original_dir = mf.ASSETS_DIR
    original_out = mf.OUTPUT_PATH
    mf.ASSETS_DIR = tmp_path / "assets"
    mf.OUTPUT_PATH = mf.ASSETS_DIR / "automation_impact_graph.png"

    try:
        path = build_automation_impact_graph()
        assert path.exists()
        assert path.stat().st_size > 0
    finally:
        mf.ASSETS_DIR = original_dir
        mf.OUTPUT_PATH = original_out
