"""Tests for search adapter formatting and live search wrapper (mocked only)."""

from unittest.mock import MagicMock, patch

from src.search_adapter import format_search_response, run_live_search
from src.search_models import SearchResponse, SearchResult


def test_format_search_response_readable_text() -> None:
    response = SearchResponse(
        query="automation jobs",
        results=[
            SearchResult(
                title="AI Agents at Work",
                url="https://example.com/agents",
                snippet="Agents automate routine tasks.",
                date="Mar 2026",
            )
        ],
        raw={"organic": []},
    )

    text = format_search_response(response)

    assert "Query: automation jobs" in text
    assert "AI Agents at Work" in text
    assert "https://example.com/agents" in text
    assert "Agents automate routine tasks." in text
    assert "Date: Mar 2026" in text


def test_run_live_search_uses_client_without_exposing_secrets() -> None:
    secret_key = "sk-super-secret-test-key"
    mock_client = MagicMock()
    mock_client.search.return_value = SearchResponse(
        query="test query",
        results=[
            SearchResult(
                title="Result",
                url="https://example.com",
                snippet="Snippet text",
            )
        ],
        raw={"organic": []},
    )

    text = run_live_search(
        query="test query",
        num_results=3,
        client=mock_client,
    )

    mock_client.search.assert_called_once_with(query="test query", num_results=3)
    assert secret_key not in text
    assert "Result" in text
    assert "https://example.com" in text


def test_run_live_search_no_real_api_call() -> None:
    mock_client = MagicMock()
    mock_client.search.return_value = SearchResponse(
        query="mocked",
        results=[],
        raw={},
    )

    with patch("src.search_adapter.SerperSearchClient", return_value=mock_client):
        text = run_live_search(query="mocked", client=mock_client)

    assert "Results: 0" in text
    mock_client.search.assert_called_once()
