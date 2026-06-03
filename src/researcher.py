import os
from typing import List, Dict, Optional, Any

from src.tavily import search as tavily_search
from src.utils import generate_queries
from src.presenter import generate_presentation

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(ROOT, "data", "research_results")
PRESENTATIONS_DIR = os.path.join(ROOT, "data", "presentations")
SUMMARIES_DIR = os.path.join(ROOT, "data", "category_summaries")


def ensure_dirs():
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    os.makedirs(PRESENTATIONS_DIR, exist_ok=True)
    os.makedirs(SUMMARIES_DIR, exist_ok=True)


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


def run_deep_research_agent(
    start_date: str,
    end_date: str,
    focus_areas: Optional[List[str]] = None,
    use_deep_agent: bool = True,
) -> Dict[str, Any]:
    """
    Run research using the Deep Research Agent for comprehensive AI topic investigation.

    This function uses LangChain's agent framework for iterative, multi-step reasoning
    that can explore unexpected findings and cross-category patterns.

    Args:
        start_date: Start date (YYYY-MM-DD or natural language)
        end_date: End date (YYYY-MM-DD or natural language)
        focus_areas: Optional list of specific categories to focus on
        use_deep_agent: If True, uses the deep agent (default: True)

    Returns:
        Dict with research status, output files, and agent output
    """
    from src.deep_research_agent import run_deep_research

    ensure_dirs()

    if use_deep_agent:
        result = run_deep_research(
            start_date=start_date,
            end_date=end_date,
            focus_areas=focus_areas,
        )
        return result
    else:
        # Fall back to simple research
        return run_research(start_date, end_date)


def run_research(start_date: str, end_date: str) -> Dict:
    """Run simple Phase 1 research: generate queries, run Tavily searches, write markdown files.

    Note: For comprehensive deep research with iterative reasoning, use run_deep_research_agent()
    with use_deep_agent=True instead.

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


def run_synthesis_and_presentation(start_date: str, end_date: str) -> Dict:
    """
    Phase 2: Synthesize research results into presentations.

    Returns a summary dict with generated presentation files.
    """
    ensure_dirs()

    # Generate markdown presentation
    presentation_file = os.path.join(PRESENTATIONS_DIR, "presentation.md")
    presentation = generate_presentation(
        RESEARCH_DIR,
        start_date=start_date,
        end_date=end_date,
        output_file=presentation_file,
    )

    written = [os.path.relpath(presentation_file, ROOT)]

    return {
        "status": "synthesis_completed",
        "presentation_file": os.path.relpath(presentation_file, ROOT),
        "files_written": written,
    }
