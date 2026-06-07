"""
Markdown Presentation Generator
Synthesizes research results into attractive HTML presentations.

This module supports:
- Template-based markdown generation (generate_presentation) — fallback only
- Deep agent-powered HTML synthesis (generate_html_presentation_with_agent)
- Markdown-to-HTML conversion (generate_html_presentation) — legacy utility
"""

import html as html_module
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any



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
    analysis and insights, use generate_html_presentation_with_agent() instead.

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


HTML_DECK_SPEC = """
Output ONLY inner slide-deck HTML (no <!DOCTYPE>, <html>, <head>, <style>, or markdown fences).
Every slide MUST use the exact class structure below. Styles are pre-defined — do not invent new classes.

REQUIRED SLIDES (in order, 8–9 total)
1. cover — title + subtitle + meta chips
2. Executive Summary — slide-intro + stat-grid + highlight-grid + callout
3. Model Releases — slide-intro + case-grid (2–3 cards) + callout
4. Tools & Frameworks — slide-intro + topic-grid (2 cards) + callout
5. Research & Papers — slide-intro + data-table-wrap table + highlight-grid
6. Company Announcements — slide-intro + case-grid + callout
7. Events & Conferences — slide-intro + topic-grid or roadmap
8. Cross-Category Insights — slide-intro + topic-grid (3–4 cards)
9. Forward Outlook — slide-intro + roadmap (4–5 items) + callout

COVER
<section class="cover">
  <div class="cover-kicker">AI Research Briefing</div>
  <h1>Compelling Title Here</h1>
  <div class="cover-subtitle">One vivid sentence capturing the month's narrative</div>
  <div class="cover-meta">
    <span class="chip">Generated {generated_at}</span>
    <span class="chip">{start_date} – {end_date}</span>
    <span class="chip screen-only">Print-ready · Ctrl+P</span>
  </div>
</section>

STANDARD SLIDE SHELL (wrap every content slide)
<section class="slide">
  <div class="slide-head">
    <div class="slide-num">01</div>
    <h2>Section Title</h2>
  </div>
  <div class="slide-body">
    <p class="slide-intro">2–3 sentence narrative opener for this section.</p>
    <!-- layout blocks below — pick the ones required for this slide type -->
  </div>
</section>

EXECUTIVE SUMMARY — include stat-grid + highlight-grid + callout
<div class="stat-grid">
  <div class="stat-card"><div class="stat-value">5</div><div class="stat-label">Categories Covered</div></div>
  <div class="stat-card"><div class="stat-value">12+</div><div class="stat-label">Key Developments</div></div>
  <div class="stat-card"><div class="stat-value">3</div><div class="stat-label">Major Themes</div></div>
  <div class="stat-card"><div class="stat-value">↑</div><div class="stat-label">Industry Momentum</div></div>
</div>
<div class="highlight-grid">
  <article class="highlight-card"><strong>Theme Title</strong><p>One concise insight sentence.</p></article>
</div>
<div class="callout"><strong>Key Takeaway:</strong> One sharp analytical sentence.</div>

CATEGORY DEEP-DIVE — case-grid with rich cards
<div class="case-grid">
  <article class="case-card">
    <h3>Item Title</h3>
    <p><strong>Date:</strong> May 28, 2026</p>
    <p><strong>Highlight:</strong> What happened and why it matters.</p>
    <p><a href="https://example.com">Source</a></p>
  </article>
</div>

CATEGORY OVERVIEW — topic-grid
<div class="topic-grid">
  <article class="topic-card">
    <div class="topic-card-head"><h3>Topic Name</h3><span class="tag">Label</span></div>
    <div class="topic-card-body">
      <p><strong>Key point:</strong> Detail here.</p>
      <ul><li>Bullet fact</li><li>Another fact</li></ul>
    </div>
  </article>
</div>

DATA SLIDE — table inside data-table-wrap
<div class="data-table-wrap">
  <table>
    <thead><tr><th>Column</th><th>Detail</th><th>Impact</th></tr></thead>
    <tbody><tr><td>Row</td><td>Data</td><td>Significance</td></tr></tbody>
  </table>
</div>

ROADMAP / OUTLOOK — each item MUST use roadmap-content wrapper
<div class="roadmap">
  <div class="roadmap-item">
    <div class="roadmap-num">1</div>
    <div class="roadmap-content"><h3>Trend Title</h3><p>Forward-looking insight.</p></div>
  </div>
</div>

FORMATTING RULES
- Number slides 01, 02, 03… sequentially
- Every slide-body starts with slide-intro paragraph
- Use <strong> for labels (Date, Highlight, Key point) — not bare text
- Use <article> for highlight-card, case-card, topic-card
- Use <span class="tag"> inside topic-card-head (NOT chip — chip is cover-only)
- Include source <a href="..."> links from research data
- No walls of plain text — always use grids, cards, tables, or lists
- Do NOT wrap output in ```html fences
"""


def _postprocess_deck_html(deck_html: str) -> str:
    """Normalize common LLM HTML mistakes for consistent styling."""
    html = deck_html.strip()

    # chip belongs on cover only; use tag elsewhere
    parts = re.split(r'(?=<section class="slide")', html, maxsplit=0)
    if len(parts) > 1:
        html = parts[0] + "".join(p.replace('class="chip"', 'class="tag"') for p in parts[1:])

    # Wrap tables not already inside data-table-wrap
    rebuilt: list[str] = []
    pos = 0
    while True:
        start = html.find("<table>", pos)
        if start == -1:
            rebuilt.append(html[pos:])
            break
        before = html[max(0, start - 60):start]
        rebuilt.append(html[pos:start])
        end = html.find("</table>", start)
        if end == -1:
            rebuilt.append(html[start:])
            break
        end += len("</table>")
        table_block = html[start:end]
        if "data-table-wrap" in before:
            rebuilt.append(table_block)
        else:
            rebuilt.append(f'<div class="data-table-wrap">{table_block}</div>')
        pos = end
    html = "".join(rebuilt)

    # Ensure highlight-card titles use strong when LLM used h3
    html = re.sub(
        r'<article class="highlight-card">\s*<h3>(.*?)</h3>',
        r'<article class="highlight-card"><strong>\1</strong>',
        html,
        flags=re.DOTALL,
    )

    # Wrap roadmap item body content so the 2-column grid lays out correctly
    html = _fix_roadmap_items(html)

    return html


def _fix_roadmap_items(html: str) -> str:
    """Ensure each roadmap-item has roadmap-num + roadmap-content columns."""
    pattern = re.compile(
        r'(<div class="roadmap-item">\s*<div class="roadmap-num">[^<]*</div>)\s*'
        r'(.*?)\s*(</div>)',
        re.DOTALL,
    )

    def _wrap_item(match: re.Match[str]) -> str:
        prefix, content, close = match.group(1), match.group(2).strip(), match.group(3)
        if not content or content.startswith('<div class="roadmap-content">'):
            return match.group(0)
        return f'{prefix}<div class="roadmap-content">{content}</div>{close}'

    return pattern.sub(_wrap_item, html)


def _extract_deck_html(raw: str) -> str:
    """Extract slide-deck HTML from an LLM response."""
    text = raw.strip()
    if not text:
        return ""

    fence_match = re.search(r"```(?:html)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fence_match:
        text = fence_match.group(1).strip()

    if "<html" in text.lower():
        deck_match = re.search(
            r'<div class="deck">(.*)</div>\s*(?:<footer|<script|</body>)',
            text,
            re.DOTALL | re.IGNORECASE,
        )
        if deck_match:
            return deck_match.group(1).strip()
        body_match = re.search(r"<body[^>]*>(.*)</body>", text, re.DOTALL | re.IGNORECASE)
        if body_match:
            return body_match.group(1).strip()

    return text


def _wrap_html_document(title: str, deck_html: str) -> str:
    """Wrap deck sections in a complete styled HTML document."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html_module.escape(title)}</title>
  <style>
{SCREEN_STYLES}
{PRINT_STYLES}
  </style>
</head>
<body>
  <div class="deck">
    {deck_html}
    <footer class="footer">AI Research Agent · Designed for screen viewing and print/PDF export</footer>
  </div>
</body>
</html>
"""


def _html_from_markdown_content(markdown_content: str, title: Optional[str] = None) -> str:
    """Build a full HTML document from markdown using the template renderer."""
    doc_title = title or _extract_title(markdown_content)
    generated_at = datetime.now().strftime("%B %d, %Y")
    deck_html = _build_slide_deck(markdown_content, generated_at)
    return _wrap_html_document(doc_title, deck_html)


def generate_html_presentation_with_agent(
    research_dir: str,
    start_date: str,
    end_date: str,
    output_file: Optional[str] = None,
    llm: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Generate a styled HTML presentation using the Deep Synthesis Agent.

    The agent analyzes research findings and outputs slide-deck HTML that uses
    the project's design system (cover slide, cards, grids, print-ready layout).
    """
    research = load_research_files(research_dir)

    if not research:
        empty_html = _wrap_html_document(
            "AI Research Presentation",
            '<section class="slide"><div class="slide-body"><p>No research files found.</p></div></section>',
        )
        return {
            "status": "no_data",
            "message": "No research files found",
            "html": empty_html,
        }

    research_summary = _build_research_summary(research, start_date, end_date)
    generated_at = datetime.now().strftime("%B %d, %Y")

    from src.deep_research_agent import create_synthesis_agent

    agent = create_synthesis_agent(llm)

    synthesis_task = f"""Create a polished, visually rich HTML slide deck about AI developments from {start_date} to {end_date}.

Research Data:
{research_summary}

Design goals:
- Eye-catching, magazine-quality layout using the provided CSS components
- Each section must follow its prescribed layout (stat-grid, case-grid, topic-grid, tables, roadmap)
- Sharp, analytical writing — not generic summaries
- Include specific dates, names, and source links from the research data

{HTML_DECK_SPEC.format(generated_at=generated_at, start_date=start_date, end_date=end_date)}

Use {generated_at} in the cover chip."""

    doc_title = f"AI Landscape Report: {start_date} to {end_date}"

    try:
        result = agent.invoke(
            {"messages": [("human", synthesis_task)]},
            config={"recursion_limit": 20},
        )
        messages = result.get("messages", [])
        raw_output = messages[-1].content if messages else ""
        deck_html = _postprocess_deck_html(_extract_deck_html(raw_output))

        if not deck_html or "<section" not in deck_html.lower():
            raise ValueError("Agent did not return valid slide-deck HTML")

        html = _wrap_html_document(doc_title, deck_html)

        if output_file:
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)

        return {
            "status": "success",
            "html": html,
            "output_file": output_file,
            "categories_analyzed": list(research.keys()),
        }

    except Exception as e:
        fallback_md = generate_presentation(research_dir, start_date, end_date)
        html = _html_from_markdown_content(fallback_md, title=doc_title)

        if output_file:
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)

        return {
            "status": "fallback",
            "message": f"Agent HTML synthesis failed, using template renderer: {e}",
            "html": html,
            "output_file": output_file,
            "categories_analyzed": list(research.keys()),
        }


def generate_presentation_with_agent(
    research_dir: str,
    start_date: str,
    end_date: str,
    output_file: Optional[str] = None,
    llm: Optional[Any] = None,
) -> Dict[str, Any]:
    """Deprecated alias — use generate_html_presentation_with_agent instead."""
    if output_file and output_file.endswith(".md"):
        html_file = output_file.replace(".md", ".html")
    elif output_file:
        html_file = output_file
    else:
        html_file = None

    result = generate_html_presentation_with_agent(
        research_dir, start_date, end_date, output_file=html_file, llm=llm
    )
    result["presentation"] = result.get("html", "")
    return result


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


PRINT_STYLES = """
@media print {
  @page {
    size: A4 landscape;
    margin: 12mm;
  }

  html { font-size: 10pt; }

  body {
    background: #ffffff !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .deck { gap: 0; padding: 0; }

  .slide {
    break-after: page;
    page-break-after: always;
    box-shadow: none !important;
    border: 1px solid #dbeafe;
    min-height: auto;
  }

  .slide:last-child {
    break-after: auto;
    page-break-after: auto;
  }

  .cover,
  .topic-card,
  .highlight-card,
  .case-card,
  .callout,
  .stat-card,
  .roadmap-item,
  table,
  tr {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  .screen-only { display: none !important; }

  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #64748b;
  }
}
"""


SCREEN_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --ink: #0f172a;
  --muted: #64748b;
  --paper: #ffffff;
  --bg: #eef2ff;
  --brand: #4f46e5;
  --brand-dark: #312e81;
  --cyan: #06b6d4;
  --violet: #8b5cf6;
  --rose: #f43f5e;
  --amber: #f59e0b;
  --emerald: #10b981;
  --line: rgba(99, 102, 241, 0.14);
  --shadow: 0 24px 60px rgba(15, 23, 42, 0.12);
  --shadow-sm: 0 8px 24px rgba(15, 23, 42, 0.08);
  --radius: 22px;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  color: var(--ink);
  font-family: "DM Sans", "Segoe UI", sans-serif;
  background:
    radial-gradient(circle at 0% 0%, rgba(79, 70, 229, 0.18), transparent 32%),
    radial-gradient(circle at 100% 0%, rgba(6, 182, 212, 0.16), transparent 28%),
    linear-gradient(180deg, #f8fafc 0%, var(--bg) 100%);
}

.deck {
  max-width: 1180px;
  margin: 0 auto;
  padding: 28px 20px 56px;
  display: grid;
  gap: 32px;
}

/* ── Cover ── */
.cover {
  position: relative;
  overflow: hidden;
  border-radius: calc(var(--radius) + 4px);
  padding: 64px 56px 52px;
  color: #f8fafc;
  background:
    radial-gradient(circle at 85% 15%, rgba(34, 211, 238, 0.35), transparent 28%),
    radial-gradient(circle at 10% 90%, rgba(139, 92, 246, 0.38), transparent 32%),
    linear-gradient(135deg, #0f172a 0%, #1e1b4b 42%, #312e81 100%);
  box-shadow: var(--shadow);
}

.cover::before {
  content: "";
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.6;
}

.cover::after {
  content: "";
  position: absolute;
  inset: auto -80px -80px auto;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
}

.cover-kicker {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.78rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-weight: 700;
}

.cover h1 {
  position: relative;
  z-index: 1;
  margin: 24px 0 18px;
  max-width: 920px;
  font-family: "Space Grotesk", "Segoe UI", sans-serif;
  font-size: clamp(2.4rem, 5vw, 4rem);
  line-height: 1.05;
  letter-spacing: -0.03em;
  text-shadow: 0 2px 24px rgba(0, 0, 0, 0.25);
}

.cover-subtitle {
  position: relative;
  z-index: 1;
  max-width: 720px;
  font-size: 1.15rem;
  line-height: 1.75;
  color: rgba(248, 250, 252, 0.88);
}

.cover-meta {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.14);
  font-size: 0.88rem;
  font-weight: 500;
}

/* ── Slides ── */
.slide {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.slide-head {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 22px 28px;
  background: linear-gradient(90deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.06));
  border-bottom: 1px solid var(--line);
}

.slide-num {
  flex: 0 0 auto;
  width: 50px;
  height: 50px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--brand), var(--cyan));
  color: white;
  font-family: "Space Grotesk", sans-serif;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
}

.slide-head h2 {
  margin: 0;
  font-family: "Space Grotesk", sans-serif;
  font-size: clamp(1.35rem, 2.4vw, 1.95rem);
  line-height: 1.2;
  color: var(--brand-dark);
}

.slide-body {
  padding: 28px 30px 34px;
}

.slide-intro {
  margin: 0 0 24px;
  padding: 16px 20px;
  font-size: 1.06rem;
  line-height: 1.75;
  color: #334155;
  background: linear-gradient(90deg, rgba(79, 70, 229, 0.05), transparent);
  border-left: 4px solid var(--brand);
  border-radius: 0 12px 12px 0;
}

/* ── Stats strip ── */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 14px;
  margin-bottom: 22px;
}

.stat-card {
  text-align: center;
  padding: 18px 14px;
  border-radius: 16px;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  border: 1px solid #e2e8f0;
  box-shadow: var(--shadow-sm);
}

.stat-value {
  font-family: "Space Grotesk", sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.1;
  background: linear-gradient(135deg, var(--brand), var(--cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  margin-top: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* ── Tags (in-slide badges) ── */
.tag {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.14), rgba(6, 182, 212, 0.1));
  color: var(--brand-dark);
  border: 1px solid rgba(79, 70, 229, 0.2);
  white-space: nowrap;
}

/* ── Topic cards ── */
.topic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
}

.topic-card {
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.topic-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 32px rgba(15, 23, 42, 0.1);
}

.topic-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.07));
  border-bottom: 1px solid #e2e8f0;
}

.topic-card-head h3 {
  margin: 0;
  flex: 1;
  font-family: "Space Grotesk", sans-serif;
  font-size: 1.02rem;
  line-height: 1.35;
  color: var(--brand-dark);
}

.topic-card-body {
  padding: 16px 18px 18px;
  font-size: 0.96rem;
  line-height: 1.65;
  color: #334155;
}

.topic-card-body p { margin: 0 0 10px; }
.topic-card-body p:last-child { margin-bottom: 0; }
.topic-card-body ul, .topic-card-body ol { margin: 8px 0 0; padding-left: 1.2rem; }
.topic-card-body li + li { margin-top: 0.35rem; }

/* ── Highlight cards ── */
.highlight-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 18px 0;
}

.highlight-card {
  position: relative;
  padding: 20px 18px 18px;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.highlight-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--brand), var(--cyan));
}

.highlight-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 32px rgba(15, 23, 42, 0.1);
}

.highlight-card strong,
.highlight-card h3 {
  display: block;
  margin: 0 0 10px;
  font-family: "Space Grotesk", sans-serif;
  font-size: 1rem;
  line-height: 1.3;
  color: var(--brand-dark);
}

.highlight-card p {
  margin: 0;
  font-size: 0.94rem;
  line-height: 1.6;
  color: #475569;
}

/* ── Case study cards ── */
.case-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  margin: 18px 0;
}

.case-card {
  padding: 22px 22px 20px;
  border-radius: 18px;
  border: 1px solid #e9d5ff;
  border-left: 5px solid var(--violet);
  background: linear-gradient(180deg, #faf5ff 0%, #ffffff 100%);
  box-shadow: var(--shadow-sm);
}

.case-card h3 {
  margin: 0 0 14px;
  font-family: "Space Grotesk", sans-serif;
  font-size: 1.05rem;
  line-height: 1.35;
  color: #5b21b6;
}

.case-card p {
  margin: 0 0 10px;
  font-size: 0.95rem;
  line-height: 1.65;
  color: #334155;
}

.case-card p:last-child { margin-bottom: 0; }

.case-card ul, .case-card ol {
  margin: 8px 0 0;
  padding-left: 1.2rem;
  font-size: 0.94rem;
  line-height: 1.6;
  color: #334155;
}

.case-card li + li { margin-top: 0.35rem; }

/* ── Callout ── */
.callout {
  margin-top: 22px;
  padding: 18px 22px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.07));
  border: 1px solid rgba(16, 185, 129, 0.22);
  font-size: 1rem;
  line-height: 1.7;
  color: #1e293b;
}

.callout strong,
.callout h3 {
  display: block;
  margin: 0 0 8px;
  font-family: "Space Grotesk", sans-serif;
  font-size: 1rem;
  color: #047857;
}

.callout p {
  margin: 0;
}

/* ── Roadmap ── */
.roadmap {
  display: grid;
  gap: 14px;
  margin: 18px 0;
}

.roadmap-item {
  display: grid;
  grid-template-columns: 46px 1fr;
  gap: 16px;
  align-items: start;
  padding: 18px 20px;
  border-radius: 16px;
  background: linear-gradient(90deg, #f8fafc 0%, #ffffff 100%);
  border: 1px solid #e2e8f0;
  box-shadow: var(--shadow-sm);
}

.roadmap-num {
  grid-column: 1;
  grid-row: 1 / -1;
  width: 46px;
  height: 46px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--brand), var(--violet));
  color: white;
  font-family: "Space Grotesk", sans-serif;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
  align-self: start;
}

.roadmap-content {
  grid-column: 2;
  min-width: 0;
}

.roadmap-item > h3,
.roadmap-content h3 {
  margin: 0 0 6px;
  font-family: "Space Grotesk", sans-serif;
  font-size: 1rem;
  line-height: 1.35;
  color: var(--brand-dark);
}

.roadmap-item > p,
.roadmap-content p {
  margin: 0;
  font-size: 0.94rem;
  line-height: 1.65;
  color: #475569;
}

/* Direct h3/p siblings (before postprocess) still align in column 2 */
.roadmap-item > h3 {
  grid-column: 2;
}

.roadmap-item > p {
  grid-column: 2;
}

/* ── Tables ── */
.data-table-wrap {
  overflow: hidden;
  border-radius: 18px;
  border: 1px solid #dbeafe;
  margin: 18px 0;
  box-shadow: var(--shadow-sm);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.94rem;
}

thead {
  background: linear-gradient(90deg, #312e81, #4f46e5);
  color: white;
}

th {
  padding: 14px 16px;
  text-align: left;
  font-family: "Space Grotesk", sans-serif;
  font-weight: 600;
  font-size: 0.88rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

td {
  padding: 14px 16px;
  text-align: left;
  vertical-align: top;
  line-height: 1.55;
  color: #334155;
}

tbody tr:nth-child(even) { background: #f8fafc; }
tbody tr + tr td { border-top: 1px solid #e2e8f0; }
tbody tr:hover { background: rgba(79, 70, 229, 0.04); }

/* ── Typography & links ── */
.slide-body a {
  color: var(--brand);
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid rgba(79, 70, 229, 0.3);
  transition: border-color 0.15s ease;
}

.slide-body a:hover {
  border-bottom-color: var(--brand);
}

.slide-body ul, .slide-body ol {
  margin: 12px 0;
  padding-left: 1.3rem;
  line-height: 1.65;
  color: #334155;
}

.slide-body li + li { margin-top: 0.4rem; }

.prose p {
  margin: 0 0 14px;
  line-height: 1.7;
  color: #334155;
}

.prose ul, .prose ol {
  margin: 0;
  padding-left: 1.25rem;
  color: #334155;
}

.prose li + li { margin-top: 0.4rem; }

.footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.92rem;
  padding-top: 8px;
}

@media (max-width: 720px) {
  .cover { padding: 36px 24px 30px; }
  .slide-head, .slide-body { padding-left: 20px; padding-right: 20px; }
  .topic-grid, .highlight-grid, .case-grid, .stat-grid { grid-template-columns: 1fr; }
  .topic-card-head { flex-direction: column; align-items: flex-start; }
}
"""


def _extract_title(markdown_content: str, fallback: str = "AI Research Presentation") -> str:
    for line in markdown_content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _strip_leading_h1(markdown_content: str) -> str:
    lines = markdown_content.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip("\n")
    return markdown_content


def _split_markdown_sections(markdown_content: str) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    for line in _strip_leading_h1(markdown_content).splitlines():
        if line.startswith("## "):
            if current:
                sections.append(current)
            current = {"title": line[3:].strip(), "lines": []}
        elif line.strip() == "---":
            continue
        elif current is not None:
            current["lines"].append(line)

    if current:
        sections.append(current)
    return sections


def _split_h3_blocks(lines: List[str]) -> Tuple[List[str], List[Dict[str, Any]]]:
    intro: List[str] = []
    blocks: List[Dict[str, Any]] = []
    current_title: Optional[str] = None
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("### "):
            if current_title is not None:
                blocks.append({"title": current_title, "lines": current_lines})
            elif current_lines:
                intro.extend(current_lines)
            current_title = line[4:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title is not None:
        blocks.append({"title": current_title, "lines": current_lines})
    elif current_lines:
        intro.extend(current_lines)

    return intro, blocks


def _render_markdown_fragment(markdown_text: str) -> str:
    import markdown as md

    text = markdown_text.strip()
    if not text:
        return ""
    return md.markdown(text, extensions=["extra", "sane_lists", "tables", "nl2br"])


def _wrap_tables(fragment: str) -> str:
    if "<table>" not in fragment:
        return fragment
    return fragment.replace("<table>", '<div class="data-table-wrap"><table>').replace(
        "</table>", "</table></div>"
    )


def _render_highlight_list(items: List[str]) -> str:
    cards = []
    for item in items:
        item = item.strip()
        if not item.startswith("- "):
            continue
        content = _render_markdown_fragment(item[2:])
        cards.append(f'<article class="highlight-card">{content}</article>')
    return f'<div class="highlight-grid">{"".join(cards)}</div>'


def _render_roadmap(items: List[str]) -> str:
    rows = []
    for idx, item in enumerate(items, 1):
        if not item.strip():
            continue
        line = item.strip()
        if line[0].isdigit() and ". " in line:
            line = line.split(". ", 1)[1]
        content = _render_markdown_fragment(line)
        rows.append(
            f'<div class="roadmap-item"><div class="roadmap-num">{idx}</div><div>{content}</div></div>'
        )
    return f'<div class="roadmap">{"".join(rows)}</div>'


def _render_section_body(title: str, lines: List[str]) -> str:
    intro, blocks = _split_h3_blocks(lines)
    parts: List[str] = []

    if intro:
        intro_html = _wrap_tables(_render_markdown_fragment("\n".join(intro)))
        if intro_html.strip():
            parts.append(f'<div class="slide-intro prose">{intro_html}</div>')

    lower_title = title.lower()

    if blocks and ("case study" in lower_title or title.startswith("🔍")):
        cards = []
        for block in blocks:
            body = _wrap_tables(_render_markdown_fragment("\n".join(block["lines"])))
            cards.append(
                f'<article class="case-card"><h3>{html_module.escape(block["title"])}</h3>{body}</article>'
            )
        parts.append(f'<div class="case-grid">{"".join(cards)}</div>')
        return "".join(parts)

    if blocks and ("forward-looking" in lower_title or "short-term" in lower_title or "medium-term" in lower_title):
        cards = []
        for block in blocks:
            block_title = block["title"].lower()
            block_lines = block["lines"]
            if block_title.startswith("strategic questions"):
                body = _render_markdown_fragment("\n".join(block_lines))
                cards.append(
                    f'<article class="topic-card"><div class="topic-card-head"><h3>{html_module.escape(block["title"])}</h3></div>'
                    f'<div class="topic-card-body prose">{body}</div></article>'
                )
            elif any(line.strip()[:2].isdigit() for line in block_lines if line.strip()):
                cards.append(
                    f'<article class="topic-card"><div class="topic-card-head"><h3>{html_module.escape(block["title"])}</h3></div>'
                    f'<div class="topic-card-body">{_render_roadmap(block_lines)}</div></article>'
                )
            else:
                body = _wrap_tables(_render_markdown_fragment("\n".join(block_lines)))
                cards.append(
                    f'<article class="topic-card"><div class="topic-card-head"><h3>{html_module.escape(block["title"])}</h3></div>'
                    f'<div class="topic-card-body prose">{body}</div></article>'
                )
        parts.append(f'<div class="topic-grid">{"".join(cards)}</div>')
        return "".join(parts)

    if blocks:
        highlight_parts: List[str] = []
        topic_cards: List[str] = []
        callouts: List[str] = []
        for block in blocks:
            block_lines = [line for line in block["lines"] if not line.strip().lower().startswith("**bottom line")]
            for line in block["lines"]:
                if line.strip().lower().startswith("**bottom line") or "**key takeaway**" in line.lower():
                    callouts.append(f'<div class="callout">{_render_markdown_fragment(line)}</div>')

            if "key highlights" in block["title"].lower():
                highlight_parts.append(_render_highlight_list(block_lines))
                continue

            body = _wrap_tables(_render_markdown_fragment("\n".join(block_lines)))
            topic_cards.append(
                f'<article class="topic-card"><div class="topic-card-head"><h3>{html_module.escape(block["title"])}</h3></div>'
                f'<div class="topic-card-body prose">{body}</div></article>'
            )

        parts.extend(highlight_parts)
        if topic_cards:
            parts.append(f'<div class="topic-grid">{"".join(topic_cards)}</div>')
        parts.extend(callouts)
        return "".join(parts)

    prose = _wrap_tables(_render_markdown_fragment("\n".join(lines)))
    parts.append(f'<div class="prose">{prose}</div>')

    if "conclusion" in lower_title:
        for line in lines:
            if "key takeaway" in line.lower():
                parts.append(f'<div class="callout">{_render_markdown_fragment(line)}</div>')

    return "".join(parts)


def _section_has_content(lines: List[str]) -> bool:
    return any(line.strip() for line in lines)


def _prepare_deck_sections(
    sections: List[Dict[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    """Use subtitle-only sections on the cover; skip empty slides."""
    subtitle = ""
    content_sections: List[Dict[str, Any]] = []

    for section in sections:
        if _section_has_content(section["lines"]):
            content_sections.append(section)
        elif not subtitle:
            subtitle = section["title"]

    return subtitle, content_sections


def _build_slide_deck(markdown_content: str, generated_at: str) -> str:
    title = _extract_title(markdown_content)
    sections = _split_markdown_sections(markdown_content)
    subtitle, sections = _prepare_deck_sections(sections)

    if not subtitle:
        for section in sections:
            if section["title"].lower().startswith("executive summary"):
                intro, _ = _split_h3_blocks(section["lines"])
                for line in intro:
                    if line.strip() and not line.startswith("#"):
                        subtitle = _render_markdown_fragment(line.strip())
                        break
                break

    cover = f"""
<section class="cover">
  <div class="cover-kicker">AI Research Briefing</div>
  <h1>{html_module.escape(title)}</h1>
  <div class="cover-subtitle">{html_module.escape(subtitle) if subtitle else html_module.escape("Strategic analysis of the latest AI releases, research, and industry developments.")}</div>
  <div class="cover-meta">
    <span class="chip">Generated {html_module.escape(generated_at)}</span>
    <span class="chip">AI Research Agent</span>
    <span class="chip screen-only">Print-ready · Ctrl+P</span>
  </div>
</section>
"""

    slides = []
    for index, section in enumerate(sections, 1):
        body = _render_section_body(section["title"], section["lines"])
        if not body.strip():
            continue
        slides.append(
            f"""
<section class="slide">
  <div class="slide-head">
    <div class="slide-num">{index:02d}</div>
    <h2>{html_module.escape(section["title"])}</h2>
  </div>
  <div class="slide-body">{body}</div>
</section>
"""
        )

    return cover + "".join(slides)


def generate_html_presentation(
    markdown_file: str,
    output_file: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """
    Convert a markdown presentation into a styled, print-friendly HTML slide deck.

    Args:
        markdown_file: Path to the source markdown presentation
        output_file: Optional path for the generated HTML file
        title: Optional document title; inferred from the first H1 if omitted

    Returns:
        The generated HTML as a string
    """
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    doc_title = title or _extract_title(markdown_content)
    deck_html = _build_slide_deck(markdown_content, datetime.now().strftime("%B %d, %Y"))
    html = _wrap_html_document(doc_title, deck_html)

    if output_file:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

    return html
