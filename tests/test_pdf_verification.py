"""Tests for Phase 9 PDF verification script and report."""

import subprocess
from pathlib import Path

from scripts.verify_pdf_elements import (
    CHECKLIST_LABELS,
    REPORT_PATH,
    ROOT,
    run_verification,
    write_report,
)

VERIFY_SCRIPT = Path("scripts/verify_pdf_elements.py")
MAIN_PDF = Path("latex/main.pdf")
GITIGNORE = Path(".gitignore")

REQUIRED_SOURCE_FILES = (
    "latex/main.tex",
    "latex/preamble.tex",
    "latex/diagrams.tex",
    "latex/figures.tex",
    "latex/tables.tex",
    "latex/formulas.tex",
    "latex/bidi_section.tex",
    "latex/references.bib",
    "assets/automation_impact_graph.png",
    "scripts/build_pdf.py",
)


def test_verify_pdf_script_exists() -> None:
    assert VERIFY_SCRIPT.is_file()


def test_required_source_files_present() -> None:
    for relative in REQUIRED_SOURCE_FILES:
        assert Path(relative).is_file(), f"missing required file: {relative}"


def test_verification_checklist_labels_complete() -> None:
    assert len(CHECKLIST_LABELS) == 14
    assert "Hebrew-English BiDi section" in CHECKLIST_LABELS
    assert "Python-generated graph" in CHECKLIST_LABELS


def test_verification_report_can_be_generated(tmp_path: Path) -> None:
    report = run_verification()
    path = write_report(report)
    assert path == REPORT_PATH
    content = path.read_text(encoding="utf-8")
    assert "# PDF Verification Report" in content
    assert "## Required elements checklist" in content
    for label in CHECKLIST_LABELS:
        assert label in content


def test_pdf_not_tracked_by_git() -> None:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "latex/main.pdf"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0


def test_gitignore_excludes_pdf_artifacts() -> None:
    content = GITIGNORE.read_text(encoding="utf-8")
    assert "*.pdf" in content


def test_verify_pdf_script_runs_and_prints_summary() -> None:
    result = subprocess.run(
        ["uv", "run", "python", str(VERIFY_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "PDF Verification Summary" in result.stdout
    assert "OVERALL:" in result.stdout
    assert REPORT_PATH.is_file()
