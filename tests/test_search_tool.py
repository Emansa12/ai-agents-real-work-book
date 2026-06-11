"""Tests for Serper search client (mocked HTTP only; no real API calls)."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.search_tool import SerperSearchClient, SerperSearchError, _parse_response


def test_parse_organic_results() -> None:
    raw = {
        "organic": [
            {
                "title": "AI Agents in the Workplace",
                "link": "https://example.com/agents",
                "snippet": "How agents automate tasks.",
                "date": "Mar 10, 2026",
            }
        ]
    }

    response = _parse_response("automation", raw)

    assert response.query == "automation"
    assert len(response.results) == 1
    result = response.results[0]
    assert result.title == "AI Agents in the Workplace"
    assert result.url == "https://example.com/agents"
    assert result.snippet == "How agents automate tasks."
    assert result.source == "serper"
    assert result.date == "Mar 10, 2026"
    assert response.raw == raw


def test_empty_results_handled_safely() -> None:
    response = _parse_response("empty query", {"organic": []})

    assert response.results == []
    assert response.query == "empty query"


def test_missing_organic_results_handled_safely() -> None:
    response = _parse_response("no organic", {})

    assert response.results == []


def test_api_error_raises_serper_search_error() -> None:
    client = SerperSearchClient(api_key="test-serper-key")

    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"message": "Forbidden"}

    mock_http = MagicMock()
    mock_http.post.return_value = mock_response
    mock_http.__enter__.return_value = mock_http
    mock_http.__exit__.return_value = None

    with patch("src.search_tool.httpx.Client", return_value=mock_http):
        with pytest.raises(SerperSearchError, match="status 403"):
            client.search("automation jobs")


def test_http_transport_error_raises_serper_search_error() -> None:
    client = SerperSearchClient(api_key="test-serper-key")

    mock_http = MagicMock()
    mock_http.post.side_effect = httpx.ConnectError("connection failed")
    mock_http.__enter__.return_value = mock_http
    mock_http.__exit__.return_value = None

    with patch("src.search_tool.httpx.Client", return_value=mock_http):
        with pytest.raises(SerperSearchError, match="request failed"):
            client.search("automation jobs")


def test_search_returns_structured_model() -> None:
    client = SerperSearchClient(api_key="test-serper-key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "organic": [
            {
                "title": "Future of Work",
                "link": "https://example.com/work",
                "snippet": "Agents reshape jobs.",
            }
        ]
    }

    mock_http = MagicMock()
    mock_http.post.return_value = mock_response
    mock_http.__enter__.return_value = mock_http
    mock_http.__exit__.return_value = None

    with patch("src.search_tool.httpx.Client", return_value=mock_http):
        response = client.search("future of automation", num_results=3)

    assert response.query == "future of automation"
    assert len(response.results) == 1
    assert response.results[0].title == "Future of Work"
    assert response.results[0].url == "https://example.com/work"
    assert response.results[0].snippet == "Agents reshape jobs."
    assert response.results[0].source == "serper"
