"""Save crew run artifacts to outputs/ and latex/generated/."""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.redaction import redact_secrets

RESEARCH_DIR = Path("outputs/research")
DRAFTS_DIR = Path("outputs/drafts")
REVIEWS_DIR = Path("outputs/reviews")
LOGS_DIR = Path("outputs/logs")
LATEX_DIR = Path("latex/generated")


def chapter_slug(chapter_index: int) -> str:
    return f"chapter_{chapter_index:02d}"


def artifact_paths(chapter_index: int) -> dict[str, Path]:
    slug = chapter_slug(chapter_index)
    return {
        "research": RESEARCH_DIR / f"{slug}_research.md",
        "draft": DRAFTS_DIR / f"{slug}_draft.md",
        "review": REVIEWS_DIR / f"{slug}_review.md",
        "latex": LATEX_DIR / f"{slug}.tex",
        "combined": DRAFTS_DIR / f"{slug}_combined_output.md",
    }


def save_text_artifact(
    path: Path,
    content: str,
    secrets: list[str] | None = None,
) -> Path:
    """Write text to path with secret redaction. Does not print secrets."""
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_content = redact_secrets(content, secrets=secrets)
    path.write_text(safe_content, encoding="utf-8")
    return path


def save_run_metadata(
    chapter_index: int,
    chapter_title: str,
    artifact_paths_written: dict[str, str],
    notes: list[str],
    secrets: list[str] | None = None,
) -> Path:
    """Save run metadata JSON to outputs/logs/."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = chapter_slug(chapter_index)
    log_path = LOGS_DIR / f"{slug}_run_{timestamp}.json"

    payload: dict[str, Any] = {
        "chapter_index": chapter_index,
        "chapter_title": chapter_title,
        "timestamp": timestamp,
        "artifact_paths": artifact_paths_written,
        "notes": notes,
    }
    raw_json = json.dumps(payload, indent=2)
    save_text_artifact(log_path, raw_json, secrets=secrets)
    return log_path
