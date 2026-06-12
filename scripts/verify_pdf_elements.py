"""Phase 9 PDF verification — source-level checks and build artifact validation."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = ROOT / "latex"
MAIN_TEX = LATEX_DIR / "main.tex"
MAIN_PDF = LATEX_DIR / "main.pdf"
MAIN_BBL = LATEX_DIR / "main.bbl"
MAIN_LOG = LATEX_DIR / "main.log"
PREAMBLE_TEX = LATEX_DIR / "preamble.tex"
BUILD_SCRIPT = ROOT / "scripts" / "build_pdf.py"
DIAGRAMS_TEX = LATEX_DIR / "diagrams.tex"
FIGURES_TEX = LATEX_DIR / "figures.tex"
TABLES_TEX = LATEX_DIR / "tables.tex"
FORMULAS_TEX = LATEX_DIR / "formulas.tex"
BIDI_TEX = LATEX_DIR / "bidi_section.tex"
REFERENCES_BIB = LATEX_DIR / "references.bib"
ASSETS_GRAPH = ROOT / "assets" / "automation_impact_graph.png"
REPORT_PATH = ROOT / "outputs" / "logs" / "pdf_verification.md"

MIN_PAGES = 14
MAX_PAGES = 20

SECRET_PATTERNS = (
    re.compile(r"SERPER_API_KEY", re.I),
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", re.I),
    re.compile(r"OPENAI_API_KEY", re.I),
)

CHECKLIST_LABELS = (
    "cover page",
    "table of contents",
    "headers/footers",
    "chapters",
    "TikZ diagram",
    "Python-generated graph",
    "table",
    "highlighted formula",
    "Hebrew-English BiDi section",
    "citations",
    "bibliography",
    "callout/styled boxes",
    "no API keys or secrets",
    "PDF not tracked by git unless explicitly allowed",
)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class VerificationReport:
    build_datetime: str
    pdf_path: str
    page_count: int | None
    build_engine: str
    biber_succeeded: bool
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return all(check.passed for check in self.checks)

    def checklist_map(self) -> dict[str, bool]:
        mapping = {
            CHECKLIST_LABELS[0]: self._status("cover page"),
            CHECKLIST_LABELS[1]: self._status("table of contents"),
            CHECKLIST_LABELS[2]: self._status("headers/footers"),
            CHECKLIST_LABELS[3]: self._status("chapters"),
            CHECKLIST_LABELS[4]: self._status("TikZ diagram"),
            CHECKLIST_LABELS[5]: self._status("Python-generated graph"),
            CHECKLIST_LABELS[6]: self._status("table"),
            CHECKLIST_LABELS[7]: self._status("highlighted formula"),
            CHECKLIST_LABELS[8]: self._status("Hebrew-English BiDi section"),
            CHECKLIST_LABELS[9]: self._status("citations"),
            CHECKLIST_LABELS[10]: self._status("bibliography"),
            CHECKLIST_LABELS[11]: self._status("callout/styled boxes"),
            CHECKLIST_LABELS[12]: self._status("no API keys or secrets"),
            CHECKLIST_LABELS[13]: self._status("PDF not tracked by git"),
        }
        return mapping

    def _status(self, key: str) -> bool:
        for check in self.checks:
            if check.name == key:
                return check.passed
        return False


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _pdf_page_count(pdf_path: Path) -> int | None:
    try:
        import fitz  # type: ignore[import-untyped]
    except ImportError:
        return None

    if not pdf_path.is_file():
        return None
    doc = fitz.open(pdf_path)
    try:
        return len(doc)
    finally:
        doc.close()


def _detect_build_engine() -> str:
    if MAIN_LOG.is_file():
        log = _read(MAIN_LOG)
        if "XeTeX" in log or "xelatex" in log.lower():
            return "XeLaTeX (XeTeX)"
        if "LuaTeX" in log or "lualatex" in log.lower():
            return "LuaLaTeX"
    build_content = _read(BUILD_SCRIPT) if BUILD_SCRIPT.is_file() else ""
    if "xelatex" in build_content.lower():
        return "XeLaTeX (configured in build script)"
    return "unknown"


def _biber_succeeded() -> bool:
    if not MAIN_BBL.is_file():
        return False
    content = _read(MAIN_BBL).strip()
    return len(content) > 0 and "\\entry" in content


def _pdf_tracked_by_git() -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "latex/main.pdf"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def _scan_latex_for_secrets() -> list[str]:
    hits: list[str] = []
    for path in LATEX_DIR.rglob("*.tex"):
        content = _read(path)
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                hits.append(f"{path.relative_to(ROOT)}: {pattern.pattern}")
    return hits


def run_verification() -> VerificationReport:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    checks: list[CheckResult] = []

    main_content = _read(MAIN_TEX) if MAIN_TEX.is_file() else ""
    preamble_content = _read(PREAMBLE_TEX) if PREAMBLE_TEX.is_file() else ""

    checks.append(
        CheckResult(
            "cover page",
            "\\begin{titlepage}" in main_content and "\\booktitle" in main_content,
            "titlepage with book title",
        )
    )
    checks.append(
        CheckResult(
            "table of contents",
            "\\tableofcontents" in main_content,
            "\\tableofcontents in main.tex",
        )
    )
    checks.append(
        CheckResult(
            "headers/footers",
            "\\pagestyle{fancy}" in main_content and "fancyhdr" in preamble_content,
            "fancy page style enabled",
        )
    )
    chapter_count = main_content.count(r"\chapter{")
    checks.append(
        CheckResult(
            "chapters",
            chapter_count >= 5,
            f"{chapter_count} chapter(s) in main.tex",
        )
    )

    diagrams_text = _read(DIAGRAMS_TEX).lower() if DIAGRAMS_TEX.is_file() else ""
    diagrams_ok = DIAGRAMS_TEX.is_file() and "tikzpicture" in diagrams_text
    checks.append(
        CheckResult(
            "TikZ diagram",
            diagrams_ok and "diagrams.tex" in main_content,
            "diagrams.tex with tikzpicture",
        )
    )

    figures_content = _read(FIGURES_TEX) if FIGURES_TEX.is_file() else ""
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

    tables_content = _read(TABLES_TEX) if TABLES_TEX.is_file() else ""
    checks.append(
        CheckResult(
            "table",
            TABLES_TEX.is_file()
            and "tabularx" in tables_content
            and "\\toprule" in tables_content,
            "tables.tex with tabularx/booktabs",
        )
    )

    formulas_content = _read(FORMULAS_TEX) if FORMULAS_TEX.is_file() else ""
    checks.append(
        CheckResult(
            "highlighted formula",
            FORMULAS_TEX.is_file() and "formulabox" in formulas_content,
            "formulas.tex with formulabox",
        )
    )

    bidi_content = _read(BIDI_TEX) if BIDI_TEX.is_file() else ""
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
            cite_count += len(re.findall(r"\\cite\{", _read(extra)))
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

    secret_hits = _scan_latex_for_secrets()
    checks.append(
        CheckResult(
            "no API keys or secrets",
            len(secret_hits) == 0,
            "no secret patterns in latex/*.tex"
            if not secret_hits
            else "; ".join(secret_hits),
        )
    )

    pdf_tracked = _pdf_tracked_by_git()
    checks.append(
        CheckResult(
            "PDF not tracked by git",
            not pdf_tracked,
            "latex/main.pdf is gitignored (not tracked)"
            if not pdf_tracked
            else "latex/main.pdf is tracked by git",
        )
    )

    page_count = _pdf_page_count(MAIN_PDF)
    page_ok = page_count is not None and MIN_PAGES <= page_count <= MAX_PAGES
    checks.append(
        CheckResult(
            "PDF exists",
            MAIN_PDF.is_file() and MAIN_PDF.stat().st_size > 0,
            str(MAIN_PDF.relative_to(ROOT)),
        )
    )
    checks.append(
        CheckResult(
            "page count valid",
            page_ok,
            f"{page_count} pages (expected {MIN_PAGES}-{MAX_PAGES})"
            if page_count is not None
            else "PDF page count unavailable (install pymupdf or build PDF)",
        )
    )

    xelatex_configured = "xelatex" in _read(BUILD_SCRIPT).lower()
    checks.append(
        CheckResult(
            "XeLaTeX build configured",
            xelatex_configured and "% !TeX program = xelatex" in main_content,
            "build_pdf.py and main.tex use XeLaTeX",
        )
    )

    return VerificationReport(
        build_datetime=now,
        pdf_path=str(MAIN_PDF.relative_to(ROOT)),
        page_count=page_count,
        build_engine=_detect_build_engine(),
        biber_succeeded=_biber_succeeded(),
        checks=checks,
    )


def render_markdown_report(report: VerificationReport) -> str:
    checklist = report.checklist_map()
    lines = [
        "# PDF Verification Report",
        "",
        f"- **Build date/time:** {report.build_datetime}",
        f"- **PDF path:** `{report.pdf_path}`",
        f"- **Page count:** "
        f"{report.page_count if report.page_count is not None else 'unknown'}",
        f"- **Build engine:** {report.build_engine}",
        f"- **Biber succeeded:** {'yes' if report.biber_succeeded else 'no'}",
        f"- **Overall result:** {'PASS' if report.all_passed else 'FAIL'}",
        "",
        "## Required elements checklist",
        "",
    ]
    for label in CHECKLIST_LABELS:
        status = "PASS" if checklist.get(label, False) else "FAIL"
        lines.append(f"- [{status}] {label}")

    lines.extend(["", "## Detailed checks", ""])
    for check in report.checks:
        status = "PASS" if check.passed else "FAIL"
        detail = f" — {check.detail}" if check.detail else ""
        lines.append(f"- [{status}] {check.name}{detail}")

    lines.append("")
    return "\n".join(lines)


def write_report(report: VerificationReport) -> Path:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_markdown_report(report), encoding="utf-8")
    return REPORT_PATH


def print_summary(report: VerificationReport) -> None:
    print("PDF Verification Summary")
    print("=" * 40)
    print(f"PDF: {report.pdf_path}")
    print(f"Pages: {report.page_count if report.page_count is not None else 'unknown'}")
    print(f"Engine: {report.build_engine}")
    print(f"Biber: {'yes' if report.biber_succeeded else 'no'}")
    print()
    for check in report.checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"  [{status}] {check.name}")
    print()
    overall = "PASS" if report.all_passed else "FAIL"
    print(f"OVERALL: {overall}")


def main() -> int:
    report = run_verification()
    report_path = write_report(report)
    print_summary(report)
    print(f"Report written to: {report_path}")
    return 0 if report.all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
