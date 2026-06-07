# 🤖 AI Research & Presentation Agent

A sophisticated deep agent that **researches the latest AI releases** for a specified time period and automatically generates an **attractive presentation** documenting the breakthroughs, trends, and key developments.

**Use Case**: Stay updated on the rapidly evolving AI landscape without manual research overhead.


## Setup Instructions

### Prerequisites

- **Python 3.12+**
- **uv** tool (lightweight Python package manager)
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Serper API Key** (for Google web search)
  - Get your key at: https://serper.dev/

### Environment Setup

2. **Configure environment variables:**
   - Copy `example.env` to `.env`
    

3. **Install dependencies with uv:**
   ```bash
   uv sync --all-extras
   ```
   This will:
   - Create a virtual environment (`.venv`)
   - Install all dependencies from `pyproject.toml`
   - Install dev dependencies (jupyter, pytest, black, ruff)
   - Prepare the project for development


## Running the Project

```bash
uv run jupyter lab notebooks/ai_research_agent.ipynb
```


### Environment Variables

- `SERPER_API_KEY` — API key for Serper Google search service
- `ANTHROPIC_API_KEY` — For Anthropic model usage (default provider)
- `ANTHROPIC_MODEL` — Anthropic model name (default: `claude-sonnet-4-20250514`)
- `LLM_PROVIDER` — Set to `anthropic` (default) or `openai`
- `OPENAI_API_KEY` — Optional fallback for OpenAI model usage
- `LANGSMITH_API_KEY` — Optional LangSmith tracing (set `LANGSMITH_TRACING=true` in `.env` to enable)

