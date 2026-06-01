import os
from typing import List, Dict

from src.tavily import search as tavily_search
from src.utils import generate_queries

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(ROOT, "data", "research_results")


def ensure_dirs():
    os.makedirs(RESEARCH_DIR, exist_ok=True)


def create_todos() -> List[Dict]:
    """Return the Phase-1 research TODOs (per-category)."""
    return [
        {"id": 1, "task": "Research Model Releases", "category": "model_releases"},
        {"id": 2, "task": "Research Tools & Frameworks", "category": "tools_frameworks"},
        {"id": 3, "task": "Research Papers", "category": "papers"},
        {"id": 4, "task": "Research Company Announcements", "category": "company_announcements"},
        {"id": 5, "task": "Research Events/Conferences", "category": "events"},
    ]


def run_tavily_search(
    query: str,
    start_date: str,
    end_date: str,
    max_results: int = 5,
    search_depth: str = "basic",
    topic: str = "general",
) -> List[Dict]:
    """Run a Tavily Search request and return a normalized result list."""
    response = tavily_search(
        query=query,
        start_date=start_date,
        end_date=end_date,
        max_results=max_results,
        search_depth=search_depth,
        topic=topic,
        include_raw_content=False,
        include_answer=False,
    )

    results = response.get("results", [])
    normalized = []
    for item in results:
        normalized.append(
            {
                "title": item.get("title", "(untitled)"),
                "url": item.get("url", ""),
                "snippet": item.get("content") or item.get("raw_content") or "",
                "score": item.get("score"),
            }
        )
    return normalized


def run_research(start_date: str, end_date: str) -> Dict:
    """Run simple Phase 1 research: generate queries, run Tavily searches, write markdown files.

    Returns a summary dict with written files.
    """
    ensure_dirs()
    queries = generate_queries(start_date, end_date)
    todos = create_todos()
    written = []

    for t in todos:
        cat = t["category"]
        q = queries.get(cat, "")
        results = run_tavily_search(q, start_date=start_date, end_date=end_date)

        fname = os.path.join(RESEARCH_DIR, f"{cat}.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"# Results for {cat}\n\n")
            f.write(f"Query: {q}\n\n")
            for r in results:
                f.write(f"- [{r['title']}]({r['url']}) — {r['snippet']}\n")
        written.append(os.path.relpath(fname, ROOT))

    return {"status": "completed", "files_written": written}
