"""Tests for token and cost estimation helpers."""

import json
from pathlib import Path

from src.cost_tracker import (
    ArtifactCostSummary,
    estimate_cost,
    estimate_tokens,
    summarize_artifact_cost,
)


def test_estimate_tokens_positive_for_nonempty_text() -> None:
    text = "abcdefghijklmnop"  # 16 chars -> 4 tokens
    assert estimate_tokens(text) == 4
    assert estimate_tokens(text) == estimate_tokens(text)


def test_estimate_tokens_empty_returns_zero() -> None:
    assert estimate_tokens("") == 0


def test_estimate_cost_nonnegative() -> None:
    cost = estimate_cost(1000, 2000, "gpt-4o-mini")
    assert cost.input_cost_usd >= 0
    assert cost.output_cost_usd >= 0
    assert cost.total_cost_usd >= 0
    assert cost.total_tokens == 3000


def test_summarize_artifact_cost_handles_missing_files() -> None:
    summary = summarize_artifact_cost(
        [Path("outputs/missing/file.md")],
        model_name="gpt-4o-mini",
    )
    assert summary.files_counted == 0
    assert summary.total_tokens == 0
    assert any("Skipped missing" in note for note in summary.notes)


def test_summarize_artifact_cost_counts_existing_file(tmp_path: Path) -> None:
    artifact = tmp_path / "chapter_01_draft.md"
    artifact.write_text("word word word word", encoding="utf-8")

    summary = summarize_artifact_cost([artifact], model_name="gpt-4o-mini")

    assert summary.files_counted == 1
    assert summary.total_tokens > 0
    assert summary.total_cost_usd >= 0


def test_report_json_contains_no_secrets(tmp_path: Path) -> None:
    secret = "sk-super-secret-report-key"
    artifact = tmp_path / "note.md"
    artifact.write_text(f"content with {secret}", encoding="utf-8")

    summary = summarize_artifact_cost(
        [artifact],
        model_name="gpt-4o-mini",
        secrets=[secret],
    )
    payload = json.dumps(summary.model_dump())

    assert secret not in payload
    assert isinstance(summary, ArtifactCostSummary)
