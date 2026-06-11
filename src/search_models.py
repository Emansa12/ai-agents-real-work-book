"""Pydantic models for internet search results."""

from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str = "serper"
    date: str | None = None


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    raw: dict
