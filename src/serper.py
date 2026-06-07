import json
import os
import ssl
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_SERPER_API_BASE = "https://google.serper.dev"
SEARCH_PATH = "/search"


def _get_api_key() -> str:
    api_key = os.getenv("SERPER_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError(
            "SERPER_API_KEY environment variable is required for Serper search."
        )
    return api_key


def _build_search_url() -> str:
    base_url = os.getenv("SERPER_API_BASE_URL", DEFAULT_SERPER_API_BASE).rstrip("/")
    return f"{base_url}{SEARCH_PATH}"


def _build_ssl_context() -> Optional[ssl.SSLContext]:
    verify_ssl = os.getenv("SSL_VERIFY", "true").lower() not in ("false", "0", "no")
    if verify_ssl:
        return None
    return ssl._create_unverified_context()


def _request(url: str, payload: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    request = Request(url=url, data=body, headers=headers, method="POST")

    try:
        with urlopen(request, timeout=30, context=_build_ssl_context()) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"Serper search HTTP error {exc.code}: {exc.reason}. Response body: {error_body}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"Serper search request failed: {exc.reason}") from exc


def _normalize_results(response: Dict[str, Any], max_results: int) -> list[Dict[str, Any]]:
    organic = response.get("organic", [])
    normalized = []

    for index, item in enumerate(organic[:max_results], start=1):
        normalized.append(
            {
                "title": item.get("title", "(untitled)"),
                "url": item.get("link", ""),
                "content": item.get("snippet", ""),
                "score": max(0.0, 1.0 - ((index - 1) * 0.08)),
                "date": item.get("date"),
            }
        )

    return normalized


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
    """
    Run a Serper Google search and return normalized results.

    search_depth, topic, and include_raw_content are accepted for API
    compatibility with callers but are not sent to Serper.
    """
    _ = search_depth, topic, include_raw_content

    api_key = _get_api_key()
    url = _build_search_url()

    payload: Dict[str, Any] = {
        "q": query,
        "num": max(1, min(max_results, 20)),
        "gl": os.getenv("SERPER_GL", "us"),
        "hl": os.getenv("SERPER_HL", "en"),
    }

    if start_date:
        payload["after"] = start_date
    if end_date:
        payload["before"] = end_date

    response = _request(url, payload, api_key)
    results = _normalize_results(response, max_results=max_results)

    output: Dict[str, Any] = {"results": results}
    if include_answer:
        answer_box = response.get("answerBox") or {}
        output["answer"] = answer_box.get("answer") or answer_box.get("snippet")

    return output
