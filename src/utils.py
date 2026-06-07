from datetime import datetime
from typing import Dict


def _parse_iso(date_str: str):
    """Try to parse an ISO-format date string to a date object.
    If parsing fails, return the original string for safe formatting.
    """
    try:
        return datetime.fromisoformat(date_str).date()
    except Exception:
        return date_str


def generate_queries(start_date: str, end_date: str) -> Dict[str, str]:
    """Generate simple, structured search queries per category for a given date range.

    Args:
        start_date: ISO date string (YYYY-MM-DD) or a free-form descriptor
        end_date: ISO date string (YYYY-MM-DD) or a free-form descriptor

    Returns:
        Dict mapping research category keys to a textual query.
    """
    s = _parse_iso(start_date)
    e = _parse_iso(end_date)
    if hasattr(s, "isoformat") and hasattr(e, "isoformat"):
        date_str = f"{s.isoformat()} to {e.isoformat()}"
    else:
        date_str = f"{start_date} - {end_date}"

    categories = {
        "model_releases": f"AI model releases {date_str}",
        "tools_frameworks": f"AI tools and frameworks releases {date_str}",
        "papers": f"machine learning papers {date_str}",
        "company_announcements": f"AI company announcements {date_str}",
        "events": f"AI events conferences {date_str}",
    }
    return categories
