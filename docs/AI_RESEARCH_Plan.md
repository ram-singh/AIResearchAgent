# 🤖 AI Research & Presentation Agent - Project Plan & Architecture

## Project Overview

A sophisticated, dual-agent collaborative workspace that researches the latest AI developments for a specified time period and automatically generates highly customized, publication-grade HTML presentations.

**Use Case**: Automating the tracking and reporting of the rapidly evolving AI landscape for researchers, developers, and product managers.

---

## 🎯 Core Features

### 1. **Time-Period Research Planning**
* Users specify a date range (e.g., month, quarter, or custom date strings) directly in the Jupyter notebook.
* The system automatically generates structured query categories:
  * **Model Releases**: LLMs, vision, and multimodal architectures.
  * **Tools & Frameworks**: Libraries, SDKs, and deployment utilities.
  * **Research Papers**: Notable publications and breakthrough methodologies.
  * **Company Announcements**: Strategic partnerships, launches, and industry updates.
  * **Events**: Conferences, workshops, and key events.

### 2. **Intelligent Research Execution (Deep Research Agent)**
* Utilizes a LangChain-based agent configured for iterative, multi-step reasoning.
* Executes searches via the Google Serper API with expanded query variations (e.g., breakthroughs, launches, and announcements).
* Saves factual findings as clean markdown documents in `data/research_results/`.

### 3. **Smart Research Caching**
* Avoids redundant search engine queries and LLM tokens.
* If non-empty markdown findings exist in `data/research_results/` for the current workspace, the research execution phase is skipped, and the synthesis pipeline is launched directly on the cached findings.

### 4. **Aesthetic Presentation Synthesis (Synthesis Agent)**
* Utilizes a specialized synthesis agent that reads the collected research markdown.
* Formats content directly into custom visual layouts using a pre-defined CSS class system (`cover`, `slide`, `stat-grid`, `highlight-grid`, `case-grid`, `topic-grid`, `roadmap`, `callout`).
* Outputs a magazine-quality, fully responsive, print-friendly HTML slide deck (`presentation.html`).
* Automatically falls back to a template-based markdown renderer if agent-powered HTML generation fails.

### 5. **Robust Runtime Environment**
* Supports environment toggles for corporate proxies (by setting `SSL_VERIFY=false` to patch HTTPX clients).
* Full LangSmith tracing configuration (`LANGSMITH_TRACING=true`) for step-by-step agent debugging.

## 🔧 Technical Architecture & Workflow (Refer architecture.drawio)

### Component Map

1. **[deep_research_agent.py](file:///c:/Repos/AIResearchAgent/src/deep_research_agent.py)**:
   * Defines search and storage tool helpers (`serper_search_tool`, `save_findings_tool`, `generate_research_queries_tool`).
   * Configures LLM providers (Anthropic Sonnet or OpenAI models).
   * Houses the core orchestrators for both `deep-research-agent` and `synthesis-agent`.
2. **[researcher.py](file:///c:/Repos/AIResearchAgent/src/researcher.py)**:
   * Sets up folders and configures env properties.
   * Manages the high-level Phase 1 (`run_research`) and Phase 2 (`run_synthesis_and_presentation`) workflows.
3. **[presenter.py](file:///c:/Repos/AIResearchAgent/src/presenter.py)**:
   * Prescribes HTML schemas (`HTML_DECK_SPEC`), layout styles (`SCREEN_STYLES`, `PRINT_STYLES`).
   * Post-processes agent output to correct styling syntax and falls back to markdown templates on failure.
4. **[serper.py](file:///c:/Repos/AIResearchAgent/src/serper.py)**:
   * Formulates requests to `google.serper.dev/search` and normalizes response datasets.
5. **[env_config.py](file:///c:/Repos/AIResearchAgent/src/env_config.py)**:
   * Parses configuration tags from `.env`, activates LangSmith tracing, and patches clients for SSL-bypassed requests.
6. **[utils.py](file:///c:/Repos/AIResearchAgent/src/utils.py)**:
   * Parses time frames and generates categorized search queries.

---

## 🚀 Implementation Phase Checklist

### Phase 1: Core Research Agent (Completed)
- [x] Configure Python runtime variables using `pyproject.toml` and `uv`.
- [x] Implement Serper query structures and client requests in `src/serper.py`.
- [x] Code structured file outputs in `src/deep_research_agent.py` to write notes category-by-category.
- [x] Establish high-level task runner inside `src/researcher.py`.

### Phase 2: Synthesis & Presentation (Completed)
- [x] Define responsive design classes and magazine elements in `src/presenter.py`.
- [x] Integrate LangChain synthesis agent to translate markdown records to structured layout sections.
- [x] Build automated fallbacks in case HTML structural synthesis fails.
- [x] Establish caching functionality to skip search steps.

### Phase 3: Runtime Stability & Usability (Completed)
- [x] Set up environment loading and proxy certificate handling in `src/env_config.py`.
- [x] Implement LangSmith project configurations.
- [x] Provide a Jupyter cell interface in `notebooks/ai_research_agent.ipynb`.

---

## 🎯 Success Criteria

1. **Autonomy**: The research agent generates query sets and refines searches without manual query crafting.
2. **Format Fidelity**: The presentation output complies with the `HTML_DECK_SPEC` rules (no markdown, clean grids, print layout support).
3. **Robustness**: If corporate networks block SSL verification, runtime configuration flags successfully bypass validation using safe local fallbacks.
4. **Efficiency**: Cached runs skip network I/O and execute in seconds.
