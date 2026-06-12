"""Tests for run_crew CLI argument handling (no live API calls)."""

import argparse
from unittest.mock import patch

import pytest

from scripts.run_crew import LIVE_API_WARNING, resolve_chapter_indices
from src.chapters import all_chapter_indices
from src.crew_runner import ChapterRunResult


def test_default_selects_chapter_one() -> None:
    args = argparse.Namespace(chapter=None, all=False)
    assert resolve_chapter_indices(args) == [1]


def test_chapter_flag_selects_requested_chapter() -> None:
    args = argparse.Namespace(chapter=2, all=False)
    assert resolve_chapter_indices(args) == [2]


def test_all_flag_selects_all_chapters() -> None:
    args = argparse.Namespace(chapter=None, all=True)
    assert resolve_chapter_indices(args) == all_chapter_indices()


def test_all_and_chapter_mutually_exclusive() -> None:
    args = argparse.Namespace(chapter=2, all=True)
    with pytest.raises(ValueError, match="not both"):
        resolve_chapter_indices(args)


@patch("scripts.run_crew.run_chapter_crew")
def test_main_default_runs_one_chapter(mock_run_chapter) -> None:
    mock_run_chapter.return_value = ChapterRunResult(
        chapter_index=1,
        chapter_title="Introduction: When AI Agents Start Doing Real Work",
        kickoff_result="done",
        artifact_paths_written={"draft": "outputs/drafts/chapter_01_draft.md"},
        notes=[],
    )

    from scripts.run_crew import main

    exit_code = main([])
    assert exit_code == 0
    mock_run_chapter.assert_called_once()


@patch("scripts.run_crew.run_chapter_crew")
def test_main_all_runs_every_chapter(mock_run_chapter) -> None:
    mock_run_chapter.return_value = ChapterRunResult(
        chapter_index=1,
        chapter_title="Test",
        kickoff_result="done",
        artifact_paths_written={},
        notes=[],
    )

    from scripts.run_crew import main

    exit_code = main(["--all"])
    assert exit_code == 0
    assert mock_run_chapter.call_count == len(all_chapter_indices())


def test_live_api_warning_constant() -> None:
    assert "live" in LIVE_API_WARNING.lower()
    assert "OpenAI" in LIVE_API_WARNING or "openai" in LIVE_API_WARNING.lower()
