"""Live internet search via the Serper Google Search API."""

import httpx

from src.config import load_settings
from src.search_models import SearchResponse, SearchResult

SERPER_SEARCH_URL = "https://google.serper.dev/search"


class SerperSearchError(Exception):
    """Raised when the Serper API request fails or returns an invalid response."""


class SerperSearchClient:
    """Client for live Google search results through Serper."""

    def __init__(self, api_key: str | None = None, timeout: float = 30.0) -> None:
        if api_key is None:
            settings = load_settings()
            api_key = settings.serper_api_key
        self._api_key = api_key
        self._timeout = timeout

    def search(self, query: str, num_results: int = 5) -> SearchResponse:
        """Run a live Serper search and return structured results."""
        headers = {
            "X-API-KEY": self._api_key,
            "Content-Type": "application/json",
        }
        payload = {"q": query, "num": num_results}

        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    SERPER_SEARCH_URL,
                    headers=headers,
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise SerperSearchError(
                f"Serper search request failed for query '{query}': {exc}"
            ) from exc

        if response.status_code != 200:
            raise SerperSearchError(
                f"Serper search failed with status {response.status_code} "
                f"for query '{query}'."
            )

        try:
            raw = response.json()
        except ValueError as exc:
            raise SerperSearchError(
                f"Serper search returned invalid JSON for query '{query}'."
            ) from exc

        return _parse_response(query=query, raw=raw)


def _parse_response(query: str, raw: dict) -> SearchResponse:
    organic = raw.get("organic") or []
    results: list[SearchResult] = []

    for item in organic:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        url = str(item.get("link") or "").strip()
        snippet = str(item.get("snippet") or "").strip()
        date_value = item.get("date")
        date = str(date_value).strip() if date_value else None

        results.append(
            SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source="serper",
                date=date,
            )
        )

    return SearchResponse(query=query, results=results, raw=raw)
