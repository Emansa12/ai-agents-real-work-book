"""Helper utilities for PDF verification checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from src.pdf_verification import (
    BUILD_SCRIPT,
    LATEX_DIR,
    MAIN_BBL,
    MAIN_LOG,
    ROOT,
    SECRET_PATTERNS,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def pdf_page_count(pdf_path: Path) -> int | None:
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


def detect_build_engine() -> str:
    if MAIN_LOG.is_file():
        log = read_text(MAIN_LOG)
        if "XeTeX" in log or "xelatex" in log.lower():
            return "XeLaTeX (XeTeX)"
        if "LuaTeX" in log or "lualatex" in log.lower():
            return "LuaLaTeX"
    build_content = read_text(BUILD_SCRIPT) if BUILD_SCRIPT.is_file() else ""
    if "xelatex" in build_content.lower():
        return "XeLaTeX (configured in build script)"
    return "unknown"


def biber_succeeded() -> bool:
    if not MAIN_BBL.is_file():
        return False
    content = read_text(MAIN_BBL).strip()
    return len(content) > 0 and "\\entry" in content


def pdf_tracked_by_git() -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "latex/main.pdf"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def scan_latex_for_secrets() -> list[str]:
    hits: list[str] = []
    for path in LATEX_DIR.rglob("*.tex"):
        content = read_text(path)
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                hits.append(f"{path.relative_to(ROOT)}: {pattern.pattern}")
    return hits
