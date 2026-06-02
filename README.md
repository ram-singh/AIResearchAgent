# 🤖 AI Research & Presentation Agent

A sophisticated deep agent that **researches the latest AI releases** for a specified time period and automatically generates an **attractive presentation** documenting the breakthroughs, trends, and key developments.

**Use Case**: Stay updated on the rapidly evolving AI landscape without manual research overhead.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [Development](#development)

---

## Project Overview

### Core Features

1. **Time-Period Research Planning**
   - Accept user input directly in Jupyter notebook: specific date range
   - Parse input to create structured research queries
   - Plan research across multiple AI domains:
     - Model Releases
     - Tools & Frameworks
     - Research Papers
     - Company Announcements
     - Events & Conferences

2. **Intelligent Research Execution**
   - Conduct parallel searches across different AI categories
   - Leverage Tavily search API for live web searches
   - Store research results as organized markdown files

3. **Content Synthesis & Analysis**
   - Extract key information from research results
   - Identify trends and patterns across releases
   - Categorize innovations by type and impact

4. **Presentation Generation**
   - Generate markdown-only presentations
   - Executive summary with trends
   - Timeline visualization
   - Category breakdowns with insights
   - Comparison tables and highlights

---

## Setup Instructions

### Prerequisites

- **Python 3.12+**
- **uv** tool (lightweight Python package manager)
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Tavily API Key** (for live searches)
  - Get your key at: https://tavily.com/

### Environment Setup

1. **Clone or navigate to the project:**
   ```bash
   cd /Users/Ram/Desktop/AIResearchAgent
   ```

2. **Configure environment variables:**
   - Copy `example.env` to `.env`:
     ```bash
     cp example.env .env
     ```
   - Edit `.env` and add your Tavily API key (already present with dev key)

3. **Install dependencies with uv:**
   ```bash
   uv sync --all-extras
   ```
   This will:
   - Create a virtual environment (`.venv`)
   - Install all dependencies from `pyproject.toml`
   - Install dev dependencies (jupyter, pytest, black, ruff)
   - Prepare the project for development

---

## Running the Project

### Quick Start: Jupyter Notebook

The recommended way to run the research agent:

```bash
uv run jupyter lab notebooks/ai_research_agent.ipynb
```

**Note:** Make sure dev dependencies are installed with `uv sync --all-extras` first.

Then in the notebook:
1. **Edit the date range** in the first cell:
   ```python
   start_date = "2026-05-01"
   end_date = "2026-05-31"
   ```
2. **Run all cells** to execute the research agent
3. **View results** in `data/research_results/` directory

The notebook will generate markdown files for each research category.

### Programmatic Usage

Execute the research agent directly from Python:

```bash
uv run python -c "from src.researcher import run_research; print(run_research('2026-05-01', '2026-05-31'))"
```

### Run Tests

```bash
uv run pytest
```

---

## Project Structure

```
AIResearchAgent/
├── data/
│   ├── research_results/       # Raw search results (per-category markdown)
│   ├── category_summaries/     # Collated markdown summaries
│   └── presentations/          # Generated presentation.md
│
├── notebooks/
│   └── ai_research_agent.ipynb    # Main research workflow notebook
│
├── src/
│   ├── researcher.py           # Core research execution logic
│   ├── tavily.py               # Tavily search API client
│   └── utils.py                # Utility functions (date parsing, query generation)
│
├── pyproject.toml              # Project metadata and dependencies
├── .env                        # Environment variables (API keys)
├── example.env                 # Example environment template
├── AI_RESEARCH_Plan.md         # Detailed project plan
└── README.md                   # This file
```

---

## Development

### Adding Dependencies

Add new dependencies to `pyproject.toml`:

```bash
uv pip install <package_name>
```

Or edit `pyproject.toml` and run:
```bash
uv sync --all-extras
```

### Code Quality

Format code with Black:
```bash
uv run black src/ notebooks/
```

Check code with Ruff:
```bash
uv run ruff check src/
```

### Environment Variables

**Required:**
- `TAVILY_API_KEY` — API key for Tavily search service

**Optional:**
- `ANTHROPIC_API_KEY` — For Anthropic model usage
- `OPENAI_API_KEY` — For OpenAI model usage
- `LANGSMITH_API_KEY` — For LangSmith tracing

---

## Example Usage

### Research AI Releases for a Date Range

1. **Start Jupyter:**
   ```bash
   uv run jupyter lab notebooks/ai_research_agent.ipynb
   ```

2. **In the notebook, edit the first cell with your date range:**
   ```python
   start_date = "2026-05-01"
   end_date = "2026-05-31"
   ```

3. **Run all cells** to execute the research workflow

4. **View results:**
   - Check `data/research_results/` for markdown files
   - Each research category has a `.md` file with organized search results

---

## Success Criteria

- ✅ Notebook accepts date range as cell variables (`start_date`, `end_date`)
- ✅ Agent finds 10+ relevant AI releases per category
- ✅ Generates markdown files with organized research results
- ✅ Efficiently manages research state with organized output files
- ✅ Full research cycle completes in minutes

---

## Troubleshooting

**`uv sync` fails:**
- Ensure Python 3.12+ is installed: `python3 --version`
- Delete `.venv` and try again: `rm -rf .venv && uv sync`

**Tavily search returns empty results:**
- Check `.env` file has valid `TAVILY_API_KEY`
- Verify API key is active at https://tavily.com/

**Jupyter notebook not found:**
- Ensure you're in the correct directory
- Run from `/Users/Ram/Desktop/AIResearchAgent`

---

## License & Contributing

See `AI_RESEARCH_Plan.md` for detailed project specifications.