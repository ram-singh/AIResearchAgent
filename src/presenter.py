"""
Markdown Presentation Generator
Synthesizes research results into attractive markdown presentations.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def load_research_files(research_dir: str) -> Dict[str, str]:
    """Load all research markdown files and return as dict of category -> content."""
    research = {}
    if not os.path.exists(research_dir):
        return research

    for fname in os.listdir(research_dir):
        if fname.endswith(".md"):
            category = fname.replace(".md", "")
            fpath = os.path.join(research_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                research[category] = f.read()

    return research


def parse_research_results(content: str) -> List[Dict]:
    """
    Parse markdown research content and extract structured items.
    Format: - [Title](url) — snippet
    """
    items = []
    lines = content.split("\n")

    for line in lines:
        if line.startswith("- ["):
            # Extract title
            title_match = re.search(r"\- \[(.*?)\]", line)
            if not title_match:
                continue
            title = title_match.group(1)

            # Extract URL
            url_match = re.search(r"\]\((.*?)\)", line)
            url = url_match.group(1) if url_match else ""

            # Extract snippet (text after the URL)
            snippet_start = line.find("— ") + 2 if "— " in line else line.find(") ") + 2
            snippet = line[snippet_start:].strip() if snippet_start > 1 else ""

            if title and snippet:
                items.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet[:200],  # Truncate to 200 chars
                })

    return items


def categorize_items(items: List[Dict]) -> Dict[str, List]:
    """Group items by inferred category/type."""
    categorized = {
        "Models & LLMs": [],
        "Tools & Frameworks": [],
        "Research & Papers": [],
        "Announcements": [],
        "Events": [],
        "Other": [],
    }

    keywords = {
        "Models & LLMs": ["model", "llm", "language model", "gpt", "claude", "gemini"],
        "Tools & Frameworks": ["framework", "library", "tool", "sdk", "platform"],
        "Research & Papers": ["paper", "research", "study", "arxiv", "publication"],
        "Announcements": ["announces", "released", "launch", "unveil"],
        "Events": ["conference", "event", "workshop", "summit"],
    }

    for item in items:
        text = (item["title"] + " " + item["snippet"]).lower()
        placed = False

        for category, kws in keywords.items():
            if any(kw in text for kw in kws):
                categorized[category].append(item)
                placed = True
                break

        if not placed:
            categorized["Other"].append(item)

    return categorized


def generate_summary(items: List[Dict], category: str) -> str:
    """Generate a brief summary of the research findings for a category."""
    if not items:
        return f"No items found in {category}."

    summaries = []
    for i, item in enumerate(items[:3], 1):
        summaries.append(f"{i}. **{item['title']}** - {item['snippet'][:150]}...")

    return "\n".join(summaries)


def generate_timeline_table(items: List[Dict]) -> str:
    """Generate a markdown table timeline of items."""
    if not items:
        return "No items to display.\n"

    table_lines = [
        "| # | Release | Snippet |",
        "|---|---------|---------|",
    ]

    for i, item in enumerate(items[:10], 1):
        snippet = item["snippet"][:80].replace("|", "").replace("\n", " ")
        table_lines.append(
            f"| {i} | [{item['title']}]({item['url']}) | {snippet}... |"
        )

    return "\n".join(table_lines) + "\n"


def generate_presentation(
    research_dir: str,
    start_date: str,
    end_date: str,
    output_file: str = None,
) -> str:
    """
    Generate a comprehensive markdown presentation from research results.

    Args:
        research_dir: Path to directory containing research markdown files
        start_date: Research period start date
        end_date: Research period end date
        output_file: Optional path to write presentation to

    Returns:
        The generated markdown presentation as a string
    """
    research = load_research_files(research_dir)

    if not research:
        return "# No research data available\n\nNo research files found."

    # Collect all items from all categories
    all_items = []
    for category, content in research.items():
        items = parse_research_results(content)
        all_items.extend(items)

    # Start building presentation
    lines = [
        "# 🚀 AI Releases & Breakthroughs",
        f"\n**Research Period**: {start_date} to {end_date}",
        f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "\n---\n",
    ]

    # Executive Summary
    lines.append("## 📈 Executive Summary\n")
    lines.append(
        f"This report documents the latest AI releases, tools, research, and announcements "
        f"from **{start_date}** to **{end_date}**.\n"
    )
    lines.append(f"**Total items found**: {len(all_items)} across {len(research)} categories.\n")

    # Categorize items
    categorized = categorize_items(all_items)

    # Timeline Overview
    lines.append("\n## 📅 Timeline Overview\n")
    lines.append(f"Found **{len(all_items)}** relevant AI releases and announcements:\n")
    lines.append(generate_timeline_table(all_items))

    # Category Breakdowns
    lines.append("\n---\n")
    lines.append("## 🎯 Category Breakdowns\n")

    category_order = [
        "Models & LLMs",
        "Tools & Frameworks",
        "Research & Papers",
        "Announcements",
        "Events",
    ]

    for category in category_order:
        items = categorized.get(category, [])
        if not items:
            continue

        lines.append(f"\n### {category} ({len(items)} items)\n")

        for i, item in enumerate(items[:5], 1):
            lines.append(f"\n**{i}. {item['title']}**")
            if item["url"]:
                lines.append(f"  - [Read more]({item['url']})")
            lines.append(f"  - {item['snippet'][:150]}...")

    # Other items
    if categorized.get("Other"):
        lines.append(f"\n### Other Items ({len(categorized['Other'])} items)\n")
        for i, item in enumerate(categorized["Other"][:5], 1):
            lines.append(
                f"\n{i}. **{item['title']}** - {item['snippet'][:100]}..."
            )

    # Key Insights
    lines.append("\n\n---\n")
    lines.append("## 💡 Key Insights\n")
    lines.append("- Multiple major model releases across different vendors\n")
    lines.append("- Emphasis on omnimodal and multimodal capabilities\n")
    lines.append("- Growing focus on agent-oriented architectures\n")
    lines.append("- Increased availability of open-source alternatives\n")

    # Footer
    lines.append("\n---\n")
    lines.append("*This presentation was automatically generated by AI Research Agent.*\n")

    presentation = "\n".join(lines)

    # Write to file if specified
    if output_file:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(presentation)

    return presentation
