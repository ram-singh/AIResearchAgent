import os
from typing import Dict, Optional, Any

from src.env_config import configure_runtime_env
from src.presenter import generate_html_presentation_with_agent

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(ROOT, "data", "research_results")
PRESENTATIONS_DIR = os.path.join(ROOT, "data", "presentations")


def ensure_dirs():
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    os.makedirs(PRESENTATIONS_DIR, exist_ok=True)


def list_research_files() -> list[str]:
    """Return relative paths of non-empty research markdown files."""
    if not os.path.isdir(RESEARCH_DIR):
        return []

    files = []
    for fname in sorted(os.listdir(RESEARCH_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(RESEARCH_DIR, fname)
        if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
            files.append(os.path.relpath(fpath, ROOT))
    return files


def run_deep_research_agent(
    start_date: str,
    end_date: str,
    focus_areas: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """
    Run research using the Deep Research Agent for comprehensive AI topic investigation.

    Skips web search when non-empty research markdown files already exist in
    data/research_results/.

    Args:
        start_date: Start date (YYYY-MM-DD or natural language)
        end_date: End date (YYYY-MM-DD or natural language)
        focus_areas: Optional list of specific categories to focus on

    Returns:
        Dict with research status, output files, and agent output
    """
    from src.deep_research_agent import run_deep_research

    ensure_dirs()
    configure_runtime_env()

    existing = list_research_files()
    if existing:
        return {
            "status": "skipped",
            "message": "Using existing research files; web search skipped.",
            "files_written": existing,
            "output_files": existing,
        }

    return run_deep_research(
        start_date=start_date,
        end_date=end_date,
        focus_areas=focus_areas,
    )


def run_research(start_date: str, end_date: str) -> Dict:
    """Run Phase 1 research using the Deep Research Agent."""
    return run_deep_research_agent(start_date, end_date)


def run_synthesis_and_presentation(start_date: str, end_date: str) -> Dict:
    """
    Phase 2: Synthesize research results into an HTML presentation using the agent.

    Returns a summary dict with the generated presentation.html path.
    """
    ensure_dirs()
    configure_runtime_env()

    html_file = os.path.join(PRESENTATIONS_DIR, "presentation.html")
    result = generate_html_presentation_with_agent(
        RESEARCH_DIR,
        start_date=start_date,
        end_date=end_date,
        output_file=html_file,
    )

    written = [os.path.relpath(html_file, ROOT)]

    return {
        "status": result.get("status", "synthesis_completed"),
        "html_file": os.path.relpath(html_file, ROOT),
        "files_written": written,
        "message": result.get("message"),
    }
