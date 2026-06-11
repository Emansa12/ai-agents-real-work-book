"""Run one live Serper search and save evidence to outputs/research/."""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from src.search_tool import SerperSearchClient, SerperSearchError

DEFAULT_QUERY = "AI agents replacing human work future of automation 2026"
OUTPUT_DIR = Path("outputs/research")


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY

    client = SerperSearchClient()

    try:
        response = client.search(query=query, num_results=5)
    except SerperSearchError as exc:
        print(f"Search error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_path = OUTPUT_DIR / f"live_search_{timestamp}.json"

    evidence = {
        "query": response.query,
        "timestamp": timestamp,
        "results": [result.model_dump() for result in response.results],
        "raw": response.raw,
    }
    output_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    print(f"Query: {response.query}")
    print(f"Results: {len(response.results)}")
    for index, result in enumerate(response.results, start=1):
        print(f"{index}. {result.title}")
        print(f"   {result.url}")
    print(f"Evidence saved to: {output_path}")


if __name__ == "__main__":
    main()
