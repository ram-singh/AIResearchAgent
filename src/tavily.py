import json
import os
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_TAVILY_API_BASE = "https://api.tavily.com"
SEARCH_PATH = "/search"


def _get_api_key() -> str:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise EnvironmentError("TAVILY_API_KEY environment variable is required for Tavily search.")
    return api_key


def _build_search_url() -> str:
    base_url = os.getenv("TAVILY_API_BASE_URL", DEFAULT_TAVILY_API_BASE).rstrip("/")
    return f"{base_url}{SEARCH_PATH}"


def _request(url: str, payload: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    request = Request(url=url, data=body, headers=headers, method="POST")

    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"Tavily search HTTP error {exc.code}: {exc.reason}. Response body: {error_body}"
        )
    except URLError as exc:
        raise RuntimeError(f"Tavily search request failed: {exc.reason}")


def search(
    query: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    max_results: int = 5,
    search_depth: str = "basic",
    topic: str = "general",
    include_raw_content: bool = False,
    include_answer: bool = False,
) -> Dict[str, Any]:
    api_key = _get_api_key()
    url = _build_search_url()
    payload: Dict[str, Any] = {
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "topic": topic,
    }

    if start_date:
        payload["start_date"] = start_date
    if end_date:
        payload["end_date"] = end_date
    if include_raw_content:
        payload["include_raw_content"] = "markdown"
    if include_answer:
        payload["include_answer"] = True

    return _request(url, payload, api_key)
