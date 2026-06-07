# 🤖 AI Research & Presentation Agent

A sophisticated, agentic AI workspace that researches the latest AI developments for a specified time period and automatically generates polished, publication-quality HTML presentations detailing model releases, research papers, software tools, events, and key industry trends.

## 🚀 Key Features

* **Two-Agent Collaborative Pipeline**:
  * **Deep Research Agent**: Iteratively searches the web, analyzes relevance, follows up on interesting leads, and saves findings to structured markdown files.
  * **Presentation Synthesis Agent**: Synthesizes the raw research files, extracts top insights, and creates a magazine-style, responsive HTML slide deck with interactive grids, timeline tables, and roadmap layouts.
* **Smart Research Caching**: Automatically skips expensive web search API calls if research results for the given period already exist in `data/research_results/`, instantly jumping to presentation synthesis.
* **Corporate Proxy/Firewall Ready**: Dynamic SSL verification override (`SSL_VERIFY=false`) and LangChain HTTPX patching support for corporate environments.
* **LangSmith Tracing Support**: Optional tracing to debug and monitor the multi-step reasoning processes of the agents.

---

## 📂 Project Structure

```
AIResearchAgent/
├── data/
│   ├── presentations/         # Output HTML slide decks
│   └── research_results/      # Saved research markdown notes (cached)
├── notebooks/
│   └── ai_research_agent.ipynb# Jupyter interface to run research & presentation tasks
├── src/
│   ├── deep_research_agent.py # Definitions for the LangChain Research & Synthesis agents
│   ├── env_config.py          # Environment settings, SSL overrides, and LangSmith setup
│   ├── presenter.py           # Presentation styling, grid components, and HTML synthesis
│   ├── researcher.py          # Orchestrates Phase 1 (Research) & Phase 2 (Synthesis)
│   ├── serper.py              # Google search client wrapping the Serper API
│   └── utils.py               # Parsing and search query generation helpers
├── .env                       # Local environment variables
├── pyproject.toml             # Python project dependencies
└── README.md                  # Project documentation
```

---

## 🛠️ Setup Instructions

### 1. Prerequisites

* **Python 3.12+**
* **uv** tool (a lightning-fast Python package manager)
  * Install via: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux) or `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows).

### 2. Environment Configuration

1. Copy the example environment template:
   ```bash
   cp example.env .env
   ```
2. Configure `.env` with your API keys:
   * **`SERPER_API_KEY`** (Required): Create a free key at [Serper.dev](https://serper.dev/) for Google searches.
   * **`ANTHROPIC_API_KEY`** (Recommended) or **`OPENAI_API_KEY`**: LLM provider API credentials.
   * **`LLM_PROVIDER`**: Set to `anthropic` (default) or `openai`.
   * **`SSL_VERIFY`**: Set to `false` if you are behind a corporate proxy that intercepts HTTPS traffic.

### 3. Install Dependencies

Install the project workspace and Jupyter development dependencies using `uv`:
```bash
uv sync --all-extras
```

---

## 🖥️ Running the Project

1. Start Jupyter Lab using `uv`:
   ```bash
   uv run jupyter lab notebooks/ai_research_agent.ipynb
   ```
2. In the notebook:
   * Edit the `start_date` and `end_date` cells to define your research timeframe.
   * Execute Phase 1 to launch the **Deep Research Agent** (saves markdown reports to `data/research_results/`).
   * Execute Phase 2 to run the **Synthesis Agent** and generate the responsive presentation in `data/presentations/presentation.html`.

---

## ⚙️ Supported Environment Variables

| Variable | Description | Default / Required |
| :--- | :--- | :--- |
| `SERPER_API_KEY` | API Key for Google Search | **Required** (for Web Search) |
| `LLM_PROVIDER` | LLM service provider (`anthropic` or `openai`) | `anthropic` |
| `ANTHROPIC_API_KEY` | API Key for Anthropic Chat Models | Required if using Anthropic |
| `ANTHROPIC_MODEL` | Model version | `claude-sonnet-4-20250514` |
| `OPENAI_API_KEY` | API Key for OpenAI Chat Models | Required if using OpenAI |
| `OPENAI_MODEL` | Model version | `gpt-4o-mini` |
| `SSL_VERIFY` | Verify SSL certificates for requests | `true` (set `false` if behind corporate firewall) |
| `LANGSMITH_TRACING` | Toggle LangSmith tracing | `false` |
| `LANGSMITH_API_KEY` | LangSmith project trace API key | Optional |
| `LANGSMITH_PROJECT` | LangSmith project workspace name | `DeepAgent` |
