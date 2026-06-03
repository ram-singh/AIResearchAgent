"""
Markdown Presentation Generator
Synthesizes research results into attractive markdown presentations.

This module supports both:
- Template-based presentation generation (generate_presentation)
- Deep agent-powered synthesis (generate_presentation_with_agent)
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from src.deep_research_agent import create_synthesis_agent, load_research_files as _load_research_files


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

    Note: For intelligent, agent-powered presentation generation with deeper
    analysis and insights, use generate_presentation_with_agent() instead.

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


def generate_presentation_with_agent(
    research_dir: str,
    start_date: str,
    end_date: str,
    output_file: Optional[str] = None,
    llm: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Generate a presentation using the Deep Synthesis Agent for intelligent analysis.

    This function uses LangChain's agent framework to analyze research findings
    and create a compelling presentation with expert insights, patterns identification,
    and cross-category analysis.

    Args:
        research_dir: Path to directory containing research markdown files
        start_date: Research period start date
        end_date: Research period end date
        output_file: Optional path to write presentation to
        llm: Optional chat model override

    Returns:
        Dict with presentation content, output file path, and agent metadata
    """
    # Load research data
    research = load_research_files(research_dir)

    if not research:
        return {
            "status": "no_data",
            "message": "No research files found",
            "presentation": "# No research data available\n\nNo research files found.",
        }

    # Build research summary for the agent
    research_summary = _build_research_summary(research, start_date, end_date)

    # Create synthesis agent
    agent = create_synthesis_agent(llm)

    # Prepare the research task
    synthesis_task = f"""Create a comprehensive, engaging presentation about AI developments from {start_date} to {end_date}.

Research Data:
{research_summary}

Requirements:
1. Executive Summary - Key highlights and most significant developments
2. Detailed Analysis by Category - Models, Tools, Papers, Announcements, Events
3. Cross-category Insights - Patterns, trends, and connections
4. Significant Examples - Specific evidence for claims
5. Forward-looking Implications - What this means for the AI landscape

Make it compelling and insightful. Go beyond summarizing - analyze and interpret.
The presentation should tell a story about the AI landscape during this period.

Output the complete presentation in markdown format."""

    try:
        result = agent.invoke({"input": synthesis_task})
        presentation = result.get("output", "")

        # Write to file if specified
        if output_file:
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(presentation)

        return {
            "status": "success",
            "presentation": presentation,
            "output_file": output_file,
            "categories_analyzed": list(research.keys()),
        }

    except Exception as e:
        # Fall back to template-based generation
        fallback_presentation = generate_presentation(
            research_dir, start_date, end_date, output_file
        )
        return {
            "status": "fallback",
            "message": f"Agent synthesis failed, using template: {str(e)}",
            "presentation": fallback_presentation,
            "output_file": output_file,
        }


def _build_research_summary(research: Dict[str, str], start_date: str, end_date: str) -> str:
    """
    Build a comprehensive summary of research data for agent consumption.

    Formats research findings in a way that's optimal for LLM analysis.
    """
    summary_parts = [f"AI Research Summary: {start_date} to {end_date}", "=" * 50, ""]

    for category, content in research.items():
        summary_parts.append(f"\n## {category.upper().replace('_', ' ')}")

        # Parse content for structured information
        lines = content.split('\n')
        items = []

        for line in lines:
            if line.startswith('- ['):
                # Extract title and URL
                title_match = re.search(r'\- \[(.*?)\]', line)
                url_match = re.search(r'\]\((.*?)\)', line)

                title = title_match.group(1) if title_match else "Untitled"
                url = url_match.group(1) if url_match else ""

                # Extract snippet
                snippet_start = line.find('— ') + 2 if '— ' in line else line.find(') ') + 2
                snippet = line[snippet_start:].strip() if snippet_start > 1 else ""

                if url:
                    items.append(f"- **{title}** ({url}): {snippet[:200]}")
                else:
                    items.append(f"- **{title}**: {snippet[:200]}")

        if items:
            summary_parts.extend(items[:10])  # Limit to 10 items per category
        else:
            # Include raw content if no structured items found
            summary_parts.append(content[:500])

        summary_parts.append("")  # Empty line between categories

    return '\n'.join(summary_parts)
