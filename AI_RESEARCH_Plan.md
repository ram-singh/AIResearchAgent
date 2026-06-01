# 🤖 AI Research & Presentation Agent

## Project Overview

A sophisticated deep agent that **researches the latest AI releases** for a specified time period and automatically generates an **attractive presentation** documenting the breakthroughs, trends, and key developments.

**Use Case**: Stay updated on the rapidly evolving AI landscape without manual research overhead.

---

## 🎯 Core Features

### 1. **Time-Period Research Planning**
- Accept user input directly in the Jupyter notebook: specific month, quarter, year, or custom date range
- Parse input to create structured research queries
- Plan research across multiple AI domains:
  - **Model Releases**: New LLMs, vision models, multimodal systems
  - **Tools & Frameworks**: New libraries, SDKs, deployment tools
  - **Research Papers**: Breakthrough publications and methodologies
  - **Company Announcements**: Major AI company updates (OpenAI, Google, Meta, etc.)
  - **Events**: Conferences, workshops, key announcements

### 2. **Intelligent Research Execution**
- Use TODO lists to organize multi-step research workflow
- Conduct parallel searches across different AI categories
- Leverage Tavily search with strategic queries:
  - "AI releases January 2025"
  - "new LLM models 2025"
  - "machine learning papers 2025"
  - "AI tools releases Q1 2025"
  - "deep learning breakthroughs 2025"
- Store research results as markdown files organized by category
- Use sub-agents (optional) for deep-dive research on specific breakthroughs

### 3. **Content Synthesis & Analysis**
- Extract key information from research:
  - Model names, capabilities, performance metrics
  - Release dates and companies
  - Key applications and use cases
  - Performance improvements over predecessors
- Identify trends and patterns across releases
- Categorize innovations by type and impact

### 4. **Attractive Presentation Generation**
Primary output: Markdown-only presentation
- Executive summary
- Timeline visualization (ASCII or markdown table)
- Category breakdowns with deep insights
- Highlight cards for major breakthroughs
- Comparison tables (performance, features)
- Visual indicators (emojis, badges)

### 5. **Context Management**
- Notebook-friendly virtual file system to store:
  - Raw research notes (per-source markdown)
  - Category-level summaries (markdown)
  - Timeline metadata (YAML/JSON metadata files kept internally)
  - Final presentation markdown (`presentation.md`)
- State isolation for multi-step synthesis: notebook cells read/write to the local VFS to offload context and preserve progress

---

## 🔧 Technical Architecture

### Agent Workflow

Input: User defines `start_date` and `end_date` in notebook cell
         ↓
1. Parse Date Range (from notebook input)
   └─ Extract time period, create research plan
         ↓
2. Create TODO List
   ├─ Research Model Releases
   ├─ Research Tools & Frameworks
   ├─ Research Papers
   ├─ Research Company Announcements
   ├─ Research Events/Conferences
   └─ [Conduct searches in parallel where possible]
         ↓
3. Execute Searches
   ├─ `run_tavily_search()` for each category
   ├─ `summarize_webpage_content()` for results
   └─ Store per-source markdown in the VFS
         ↓
4. Synthesize Findings
   ├─ `read_file()` to load summaries
   ├─ Analyze and categorize
   └─ Extract key insights and cards
         ↓
5. Generate Presentation
   ├─ Create `presentation.md` (Markdown-only)
   └─ Write to disk (`write_file()`)
         ↓
Output: `presentation.md` — clear, shareable Markdown presentation

### Key Components

1. **Research Tools** (existing)
   - `run_tavily_search()` — Web search
   - `summarize_webpage_content()` — Content summarization
   - `process_search_results()` — Result processing

2. **File System Tools** (existing)
   - `ls()` — List research files
   - `read_file()` — Load summaries for synthesis
   - `write_file()` — Store presentation outputs

3. **Task Planning** (existing)
   - `write_todos()` — Organize research workflow
   - Status tracking for multi-step research

4. **Custom Components** (to build)
   - Date parsing and query generation
   - Content synthesis and trend detection
   - Presentation formatting (Markdown)
   - Timeline visualization

---

## 📊 Example Output

### Markdown Presentation Structure
```
# 🚀 AI Releases & Breakthroughs - January 2025

## 📈 Executive Summary
[1-2 paragraph overview of major themes and trends]

## 📅 Timeline
| Date | Release | Company | Category | Impact |
|------|---------|---------|----------|--------|

## 🔬 Model Releases
### Model Name (Vendor)
- **Release Date**: YYYY-MM-DD
- **Type**: ...
- **Key Features**: ...
- **Applications**: ...

## 🛠️ Tools & Frameworks
[Organized by type with links and descriptions]

## 📚 Research Papers
[Key publications with short abstracts and direct links]

## 🌟 Top Breakthroughs
[Highlight cards for most impactful releases]

## 🎯 Key Trends
1. ...
2. ...
```

---

## 🚀 Implementation Steps

### Phase 1: Core Research Agent (Weeks 1-2)
1. Create `notebooks/ai_research_agent.ipynb` with:
   - Input cell for `start_date` and `end_date` (user edits directly in notebook)
   - Code to parse and pass date range into the research agent
2. Implement date parsing and structured query generation
3. Create structured research workflow with TODOs; test Tavily searches across domains

### Phase 2: Synthesis & Presentation (Weeks 2-3)
1. Implement content analysis and categorization
2. Build Markdown presentation generator (`presenter.py` or notebook-based generator)
3. Add comparison and timeline features; create highlight cards

### Phase 3: Optional Enhancements (Week 3-4)
1. Sub-agent for deep-dive analysis (optional)
2. Deeper trend analytics and metadata extraction (all still writing to Markdown)
3. UX improvements to the notebook-launched UI (helper widgets, short links)

---

## 💡 Why This Project Excels

✅ Notebook-first developer experience with direct date input in code cells  
✅ Reuses existing environment tooling (`uv`) for consistent dev setup  
✅ Focused output (Markdown) minimizes token confusion and maximizes shareability  
✅ Teaches agent patterns: planning, offloading, context management, and synthesis

---

## 🎯 Success Criteria

1. ✅ Notebook accepts date range as cell variables (`start_date`, `end_date`)
2. ✅ Agent finds 10+ relevant AI releases per category (where applicable)
3. ✅ Generates `presentation.md` with executive summary, timeline, and deep dives
4. ✅ Efficiently manages context offload to disk with a notebook-friendly VFS
5. ✅ Full research cycle completes in a reasonable developer run-time (target: minutes, dependent on search latencies)

---

## 🔄 Example Usage

Start dev environment, run JupyterLab, open the notebook, launch the FASTAPI UI from a cell, enter the time range, then run the notebook cells to generate `presentation.md`.

Example developer commands (using `uv`):
```bash
# sync dependencies using uv
uv sync

# launch JupyterLab
uv run jupyter lab

# optional: start the FASTAPI dev server (if running separately)
uv run python -m uvicorn src.ui:app --reload
```

---

## 📌 Notes

- `src/ui.py` is intentionally minimal — the goal is a notebook-friendly way to collect the date range and return it to the notebook agent.
- Markdown is the single, canonical output format to avoid format confusion and keep the agent token-efficient.
- The plan assumes a Python environment managed by `pyproject.toml` + `uv.lock` (no `requirements.txt`).

---

## Project Setup (canonical `uv` workflow)

### Prerequisites
- Python 3.11+ (matches `pyproject.toml`)
- `uv` tool available locally
- Tavily API access (configured via env var)

### Repository Structure (recommended)
```
/AI-Research-Agent
│
├── /data
│   ├── research_results/       # Raw per-source markdown
│   ├── category_summaries/     # Collated markdown summaries
│   └── presentations/          # Generated `presentation.md`
│
├── /notebooks
│   └── 5_ai_research_agent.ipynb
│
├── /src
│   ├── ui.py                   # Notebook-launched FASTAPI UI (`src/ui.py`)
│   ├── agent.py                # Core agent logic
│   ├── researcher.py           # Research execution and synthesis
│   ├── presenter.py            # Markdown presentation generation
│   └── utils.py                # Utility functions
│
├── pyproject.toml
├── uv.lock
└── README.md
```

### Installation / Dev commands
```bash
# install/sync dependencies with uv
uv sync

# open JupyterLab
uv run jupyter lab

# (during development) run the FASTAPI dev server (if not launched from notebook)
uv run python -m uvicorn src.ui:app --reload
```

---

If you want, I can now also create a small `src/ui.py` stub and a short notebook cell snippet demonstrating how to launch it.
# 🤖 AI Research & Presentation Agent

## Project Overview

A sophisticated deep agent that **researches the latest AI releases** for a specified time period and automatically generates an **attractive presentation** documenting the breakthroughs, trends, and key developments.

**Use Case**: Stay updated on the rapidly evolving AI landscape without manual research overhead.

---

## 🎯 Core Features

### 1. **Time-Period Research Planning**
- Accept user input: specific month, quarter, year, or custom date range
- Parse input to create structured research queries
- Plan research across multiple AI domains:
  - **Model Releases**: New LLMs, vision models, multimodal systems
  - **Tools & Frameworks**: New libraries, SDKs, deployment tools
  - **Research Papers**: Breakthrough publications and methodologies
  - **Company Announcements**: Major AI company updates (OpenAI, Google, Meta, etc.)
  - **Events**: Conferences, workshops, key announcements

### 2. **Intelligent Research Execution**
- Use TODO lists to organize multi-step research workflow
- Conduct parallel searches across different AI categories
- Leverage Tavily search with strategic queries:
  - "AI releases January 2025"
  - "new LLM models 2025"
  - "machine learning papers 2025"
  - "AI tools releases Q1 2025"
  - "deep learning breakthroughs 2025"
- Store research results as markdown files organized by category
- Use sub-agents (optional) for deep-dive research on specific breakthroughs

### 3. **Content Synthesis & Analysis**
- Extract key information from research:
  - Model names, capabilities, performance metrics
  - Release dates and companies
  - Key applications and use cases
  - Performance improvements over predecessors
- Identify trends and patterns across releases
- Categorize innovations by type and impact

### 4. **Attractive Presentation Generation**
Generate multiple output formats:

#### **A. Markdown Presentation** (Primary)
- Executive summary
- Timeline visualization (ASCII or markdown table)
- Category breakdowns with deep insights
- Highlight cards for major breakthroughs
- Comparison tables (performance, features)
- Visual indicators (emojis, badges)

#### **B. HTML Presentation** (Optional)
- Responsive design
- Interactive timeline
- Searchable release database
- Categorized galleries
- Embedded comparisons

#### **C. JSON Data Export**
- Structured data for downstream processing
- Database-ready format
- Metadata and relationships between releases

### 5. **Context Management**
- Virtual file system to store:
  - Individual research results
  - Organized category summaries
  - Final presentation files
  - Metadata and timeline data
- Efficient state management to handle large research volumes

---

## 🔧 Technical Architecture

### Agent Workflow

```
Input: "Research AI releases for January 2025"
         ↓
    1. Parse Request
       └─ Extract time period, create research plan
         ↓
    2. Create TODO List
       ├─ Research Model Releases
       ├─ Research Tools & Frameworks
       ├─ Research Papers
       ├─ Research Company Announcements
       ├─ Research Events/Conferences
       └─ [Conduct searches in parallel where possible]
         ↓
    3. Execute Searches
       ├─ tavily_search() for each category
       ├─ summarize_webpage_content() for results
       └─ Store in virtual file system
         ↓
    4. Synthesize Findings
       ├─ read_file() to load summaries
       ├─ Analyze and categorize
       └─ Extract key insights
         ↓
    5. Generate Presentation
       ├─ Create markdown presentation
       └─ write_file() to store outputs
         ↓
Output: Attractive presentation with all AI releases & trends
```

### Key Components

1. **Research Tools**
   - `run_tavily_search()` - Web search
   - `summarize_webpage_content()` - Content summarization
   - `process_search_results()` - Result processing

2. **File System Tools** 
   - `ls()` - List research files
   - `read_file()` - Load summaries for synthesis
   - `write_file()` - Store presentation outputs

3. **Task Planning** 
   - `write_todos()` - Organize research workflow
   - Status tracking for multi-step research

4. **Custom Components** (to build)
   - Date parsing and query generation
   - Content synthesis and trend detection
   - Presentation formatting (Markdown)
   - Timeline visualization
---

## 📊 Example Output

### Markdown Presentation Structure
```
# 🚀 AI Releases & Breakthroughs - January 2025

## 📈 Executive Summary
[1-2 paragraph overview of major themes and trends]

## 📅 Timeline
| Date | Release | Company | Category | Impact |
|------|---------|---------|----------|--------|

## 🔬 Model Releases
### GPT-5 (OpenAI)
- **Release Date**: Jan 15, 2025
- **Type**: Large Language Model
- **Key Features**: 2T context window, improved reasoning
- **Performance**: 95% on benchmarks vs 87% GPT-4
- **Applications**: Code generation, research assistance

[... more models ...]

## 🛠️ Tools & Frameworks
[Organized by type with links and descriptions]

## 📚 Research Papers
[Key publications with abstracts and citations]

## 🌟 Top Breakthroughs
[Highlight cards for most impactful releases]

## 🎯 Key Trends
1. Multimodal capabilities becoming standard
2. Improved reasoning on complex tasks
3. [...]
```

---

## 🚀 Implementation Steps

### Phase 1: Core Research Agent (Weeks 1-2)
1. Create `notebooks/5_ai_research_agent.ipynb`
2. Implement date parsing and query generation
3. Create structured research workflow with TODOs
4. Test Tavily searches across multiple AI domains

### Phase 2: Synthesis & Presentation (Weeks 2-3)
1. Implement content analysis and categorization
2. Build markdown presentation generator
3. Add comparison and timeline features
4. Create visual formatting with emojis/badges

### Phase 3: Advanced Features (Week 3-4)
1. HTML presentation generator (optional)
2. Sub-agent for deep-dive analysis (optional)
3. Interactive features and metadata extraction
4. Trend analysis and insight generation

---

## 💡 Why This Project Excels

✅ **Demonstrates All Deep Agent Patterns**
- Task planning (TODO lists for research workflow)
- Context offloading (file system for research storage)
- Context isolation (potential sub-agents for deep dives)

✅ **Practical & Valuable**
- Real use case: staying updated on AI landscape
- Saves significant manual research time
- Produces immediately useful artifacts

✅ **Scalable Complexity**
- Start simple (basic research + markdown)
- Add features progressively (HTML, JSON, trends)
- Optional: sub-agents for specialized analysis

✅ **Progressive Learning**
- Uses all existing tools effectively
- Introduces domain-specific challenges (synthesis, formatting)
- Teaches LLM prompt engineering for complex tasks

✅ **Impressive Deliverables**
- Beautiful markdown/HTML presentations
- Structured data for analysis
- Demonstrates agent autonomy and reasoning

---

## 🎯 Success Criteria

1. ✅ Agent can research any specified time period
2. ✅ Finds 10+ relevant AI releases per category
3. ✅ Creates visually organized presentation
4. ✅ Includes timeline, comparisons, and insights
5. ✅ Completes full research cycle in <5 minutes
6. ✅ Manages context efficiently with file system

---

## 🔄 Example Usage

```python
# User Input
query = "Research AI releases from January to March 2025 and create a presentation"

# Agent Output
# - Researches across 5 categories in parallel
# - Stores 15-20 markdown files with summaries
# - Synthesizes findings into comprehensive presentation
# - Generates presentation.md with executive summary, timeline, and deep dives
# - Exports presentation_data.json for further processing
```

---

## 📌 Notes

- **Presentation can be viewed**: Use GitHub markdown viewer for best experience
- **HTML version**: Can be hosted on GitHub Pages or any static host
- **Update frequency**: Agent can be run monthly/quarterly to track evolution
- **Customization**: Easy to adjust search queries for specific focus areas

---

## Project Setup

> Insert this after the overview section so the project plan includes concrete setup steps aligned with the repo conventions.

### Prerequisites
- Python 3.8+
- Node.js (for HTML export)
- Tavily API access

### Repository Structure
```
/AI-Research-Agent
│
├── /data
│   ├── research_results/       # Raw research data (markdown)
│   ├── presentations/          # Generated presentations (markdown, HTML)
│   └── exports/                # JSON data exports
│
├── /notebooks
│   └── 5_ai_research_agent.ipynb # Main agent notebook
│
├── /src
│   ├── agent.py                # Core agent logic
│   ├── researcher.py            # Research execution and synthesis
│   ├── presenter.py             # Presentation generation
│   └── utils.py                # Utility functions
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

### Installation
1. Clone the repo: `git clone https://github.com/yourusername/AI-Research-Agent.git`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set up Tavily API key: `export TAVILY_API_KEY='your_api_key'`

### Usage
- Run the agent notebook: `jupyter notebook notebooks/5_ai_research_agent.ipynb`
- Follow the instructions in the notebook to input your research query and generate presentations.

### Contributing
1. Fork the repo
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes
4. Commit and push: `git commit -am 'Add new feature' && git push origin feature-branch`
5. Create a pull request
