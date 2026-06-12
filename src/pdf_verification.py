"""PDF verification constants and report types."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
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
