"""Tests for artifact path helpers and safe file writes."""

from pathlib import Path

from src.run_artifacts import (
    artifact_paths,
    chapter_slug,
    save_run_metadata,
    save_text_artifact,
)


def test_chapter_slug_format() -> None:
    assert chapter_slug(1) == "chapter_01"
    assert chapter_slug(8) == "chapter_08"


def test_artifact_paths_generated() -> None:
    paths = artifact_paths(3)

    assert paths["research"] == Path("outputs/research/chapter_03_research.md")
    assert paths["draft"] == Path("outputs/drafts/chapter_03_draft.md")
    assert paths["review"] == Path("outputs/reviews/chapter_03_review.md")
    assert paths["latex"] == Path("latex/generated/chapter_03.tex")


def test_save_text_redacts_secrets(tmp_path: Path) -> None:
    secret = "sk-test-secret-value"
    target = tmp_path / "note.md"
    save_text_artifact(target, f"key={secret}", secrets=[secret])

    content = target.read_text(encoding="utf-8")
    assert secret not in content
    assert "***REDACTED***" in content


def test_save_run_metadata_no_secrets_in_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("src.run_artifacts.LOGS_DIR", tmp_path)
    secret = "sk-log-secret"
    log_path = save_run_metadata(
        chapter_index=1,
        chapter_title="Test Chapter",
        artifact_paths_written={"draft": "outputs/drafts/chapter_01_draft.md"},
        notes=["test note"],
        secrets=[secret],
    )

    content = log_path.read_text(encoding="utf-8")
    assert secret not in content
    assert "chapter_01" in log_path.name
