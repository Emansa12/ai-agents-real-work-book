"""Sanitize and prepare crew-generated LaTeX fragments for PDF build."""

from __future__ import annotations

import re
from pathlib import Path

LATEX_DIR = Path("latex")
GENERATED_DIR = LATEX_DIR / "generated"
BUILD_GENERATED_DIR = LATEX_DIR / ".build" / "generated"

MARKDOWN_FENCE_RE = re.compile(r"^```(?:latex|tex)?\s*$|^```\s*$")


def sanitize_tex_fragment(content: str) -> str:
    """Strip markdown code fences from crew-generated LaTeX fragments."""
    lines: list[str] = []
    for line in content.splitlines():
        if MARKDOWN_FENCE_RE.match(line.strip()):
            continue
        lines.append(line)
    text = "\n".join(lines).strip()
    if text:
        return text + "\n"
    return ""


def prepare_generated_fragments() -> list[Path]:
    """
    Copy sanitized crew fragments to latex/.build/generated/ for compilation.

    Original artifacts in latex/generated/ are not modified.
    """
    BUILD_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    prepared: list[Path] = []

    if not GENERATED_DIR.exists():
        return prepared

    for source in sorted(GENERATED_DIR.glob("*.tex")):
        sanitized = sanitize_tex_fragment(source.read_text(encoding="utf-8"))
        if not sanitized:
            continue
        target = BUILD_GENERATED_DIR / source.name
        target.write_text(sanitized, encoding="utf-8")
        prepared.append(target)

    return prepared
