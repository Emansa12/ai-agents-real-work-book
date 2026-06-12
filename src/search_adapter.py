"""Adapter between Serper search results and CrewAI tools."""

from crewai.tools import tool

from src.search_models import SearchResponse
from src.search_tool import SerperSearchClient

DEFAULT_NUM_RESULTS = 5


def format_search_response(response: SearchResponse) -> str:
    """Format a SearchResponse as readable text (no secret values)."""
    lines = [
        f"Query: {response.query}",
        f"Results: {len(response.results)}",
    ]

    for index, result in enumerate(response.results, start=1):
        lines.append(f"{index}. {result.title}")
        lines.append(f"   URL: {result.url}")
        lines.append(f"   Snippet: {result.snippet}")
        if result.date:
            lines.append(f"   Date: {result.date}")

    return "\n".join(lines)


def run_live_search(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    client: SerperSearchClient | None = None,
) -> str:
    """Run a live Serper search and return a readable summary string."""
    search_client = client or SerperSearchClient()
    response = search_client.search(query=query, num_results=num_results)
    return format_search_response(response)


@tool("Live Internet Search")
def live_internet_search(query: str) -> str:
    """
    Search the live internet via Serper for current information.

    Args:
        query: The search query string.

    Returns:
        Formatted search results with title, URL, and snippet per hit.
    """
    return run_live_search(query=query)
