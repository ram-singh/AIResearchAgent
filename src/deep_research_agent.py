"""
Deep Research Agent Module.

Uses LangChain's Agent framework for iterative, multi-step reasoning
to research AI topics with self-correction and cross-category analysis.
"""

import os
import json
from typing import Any, Dict, List, Optional, Type
from datetime import datetime

from pydantic import BaseModel, Field

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.agents import AgentFinish
from langchain_core.exceptions import ToolException
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool

from src.tavily import search as tavily_search
from src.utils import generate_queries

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(ROOT, "data", "research_results")


# =============================================================================
# Tool Input Schemas
# =============================================================================


class TavilySearchInput(BaseModel):
    """Input schema for Tavily search tool."""
    query: str = Field(
        description="The search query for researching AI news and research topics."
    )
    max_results: int = Field(
        default=10,
        description="Maximum number of search results to return (default: 10)."
    )
    search_depth: str = Field(
        default="advanced",
        description="Search depth: 'basic' or 'advanced' (default: advanced)."
    )
    topic: str = Field(
        default="ai",
        description="Topic category: 'ai', 'news', 'business', 'science', 'tech' (default: ai)."
    )


class SaveFindingsInput(BaseModel):
    """Input schema for save findings tool."""
    category: str = Field(
        description="The category name for the findings (e.g., 'model_releases', 'papers')."
    )
    findings: str = Field(
        description="The research findings to save as markdown content."
    )
    analysis_notes: str = Field(
        default="",
        description="Optional analysis notes about the significance of these findings."
    )


class QueryCategoriesInput(BaseModel):
    """Input schema for query generation tool."""
    start_date: str = Field(
        description="Start date for research in ISO format (YYYY-MM-DD) or natural language."
    )
    end_date: str = Field(
        description="End date for research in ISO format (YYYY-MM-DD) or natural language."
    )


# =============================================================================
# Tools
# =============================================================================


def tavily_search_tool(
    query: str,
    max_results: int = 10,
    search_depth: str = "advanced",
    topic: str = "ai",
) -> str:
    """
    Search for AI news, research papers, model releases, tools, and events.
    
    Use this tool to find current information about AI topics. Be specific in your
    queries to get the most relevant results. For comprehensive research, try multiple
    search queries with different angles on the same topic.
    
    Args:
        query: Specific search query about AI topics
        max_results: Number of results to return (10 recommended for research)
        search_depth: 'basic' for quick results, 'advanced' for comprehensive analysis
        topic: AI-related topic category
    
    Returns:
        JSON string containing search results with titles, URLs, snippets, and scores
    """
    try:
        response = tavily_search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            topic=topic,
            include_raw_content=False,
            include_answer=False,
        )
        results = response.get("results", [])
        
        if not results:
            return json.dumps({
                "status": "no_results",
                "query": query,
                "message": "No results found for this query. Try rephrasing."
            })
        
        # Format results nicely
        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", "Untitled"),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")[:500],  # Limit snippet length
                "score": r.get("score", 0),
            })
        
        return json.dumps({
            "status": "success",
            "query": query,
            "count": len(formatted),
            "results": formatted
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "query": query,
            "error": str(e)
        })


def save_findings_tool(
    category: str,
    findings: str,
    analysis_notes: str = "",
) -> str:
    """
    Save research findings to a markdown file for later synthesis.
    
    Use this tool to store important discoveries from your research. Include both
    factual information and your analysis of what makes these findings significant.
    
    Args:
        category: Category name (model_releases, tools_frameworks, papers, 
                  company_announcements, events)
        findings: Detailed research findings in markdown format
        analysis_notes: Your analysis of why these findings matter
    
    Returns:
        JSON confirmation with file path
    """
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    
    # Sanitize category name
    safe_category = "".join(c if c.isalnum() or c in "_-" else "_" for c in category)
    
    fname = os.path.join(RESEARCH_DIR, f"{safe_category}.md")
    timestamp = datetime.now().isoformat()
    
    content = f"""# Research Findings: {category}

**Research Date:** {timestamp}
**Category:** {category}

## Findings

{findings}

"""

    if analysis_notes:
        content += f"""## Analysis Notes

{analysis_notes}

"""
    
    content += f"""---

*Generated by Deep Research Agent*
"""
    
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    
    return json.dumps({
        "status": "saved",
        "file": os.path.relpath(fname, ROOT),
        "category": category,
        "timestamp": timestamp
    })


def generate_research_queries_tool(start_date: str, end_date: str) -> str:
    """
    Generate comprehensive search queries for AI research categories.
    
    Use this to get a structured set of queries covering all important
    AI research areas for a given time period.
    
    Args:
        start_date: Start date (YYYY-MM-DD or natural language)
        end_date: End date (YYYY-MM-DD or natural language)
    
    Returns:
        JSON object mapping categories to search queries
    """
    queries = generate_queries(start_date, end_date)
    
    # Enhance with additional query variations for deep research
    enhanced = {}
    for cat, base_query in queries.items():
        enhanced[cat] = {
            "primary": base_query,
            "variations": [
                f"{base_query} breakthrough",
                f"{base_query} announcement",
                f"{base_query} launch release",
            ]
        }
    
    return json.dumps({
        "status": "success",
        "start_date": start_date,
        "end_date": end_date,
        "categories": enhanced
    }, indent=2)


# =============================================================================
# Tool Registry
# =============================================================================


def get_research_tools() -> List[BaseTool]:
    """Get all tools available to the deep research agent."""
    return [
        BaseTool(
            name="tavily_search",
            description="Search for AI news and research. Use for specific queries about models, papers, tools, announcements, and events.",
            args_schema=TavilySearchInput,
            func=tavily_search_tool,
        ),
        BaseTool(
            name="save_findings",
            description="Save important research findings to markdown files for later synthesis.",
            args_schema=SaveFindingsInput,
            func=save_findings_tool,
        ),
        BaseTool(
            name="generate_queries",
            description="Generate structured search queries for AI research categories.",
            args_schema=QueryCategoriesInput,
            func=generate_research_queries_tool,
        ),
    ]


# =============================================================================
# Deep Research Agent
# =============================================================================


def create_deep_research_agent(llm: Optional[BaseChatModel] = None) -> AgentExecutor:
    """
    Create a deep research agent for comprehensive AI topic investigation.
    
    The agent uses iterative reasoning to:
    1. Generate comprehensive search queries
    2. Execute searches and analyze results
    3. Explore unexpected findings with follow-up searches
    4. Save structured findings for presentation generation
    
    Args:
        llm: Optional chat model. If not provided, uses OPENAI_API_KEY with gpt-4.
    
    Returns:
        Configured AgentExecutor ready for research tasks.
    """
    from langchain_openai import ChatOpenAI
    
    if llm is None:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=0.2,
        )
    
    tools = get_research_tools()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert AI Research Analyst with deep knowledge of:
- AI/ML model releases (GPT, Claude, Gemini, Llama, Mistral, etc.)
- AI tools and frameworks (LangChain, AutoGPT, Hugging Face, etc.)
- Research papers and academic publications
- Company announcements and industry news
- AI conferences and events

Your research approach:
1. Start by generating comprehensive search queries for all categories
2. Execute thorough searches - don't stop at initial results
3. Analyze each result for significance and relevance
4. Follow interesting leads with additional searches
5. Identify patterns, trends, and connections across topics
6. Save well-organized findings with your analysis

Be thorough but focused. Prioritize recent, significant developments.
Your goal is comprehensive coverage, not superficial breadth.

When you find important findings:
- Note the key facts and significance
- Consider cross-category implications
- Save findings with enough detail for later synthesis

End your research session by saving all significant findings to files."""),
        ("human", "{input}"),
        ("assistant", "{agent_scratchpad}"),
    ])
    
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=15,
        max_execution_time=300,  # 5 minute timeout
        early_stopping_method="generate",
        handle_parsing_errors=True,
    )


def run_deep_research(
    start_date: str,
    end_date: str,
    focus_areas: Optional[List[str]] = None,
    llm: Optional[BaseChatModel] = None,
) -> Dict[str, Any]:
    """
    Run comprehensive deep research on AI topics for a given time period.
    
    Args:
        start_date: Start date (YYYY-MM-DD or natural language)
        end_date: End date (YYYY-MM-DD or natural language)
        focus_areas: Optional list of specific categories to focus on
        llm: Optional chat model override
    
    Returns:
        Dict with research results and file paths
    """
    agent = create_deep_research_agent(llm)
    
    # Build research task description
    focus_text = ""
    if focus_areas:
        focus_text = f" Focus on: {', '.join(focus_areas)}."
    
    research_task = f"""Conduct comprehensive research on AI developments from {start_date} to {end_date}.{focus_text}

Research categories:
1. AI Model Releases - New models, updates, capabilities
2. Tools & Frameworks - Software releases, libraries, platforms
3. Research Papers - Notable publications, breakthroughs
4. Company Announcements - Strategic news, partnerships, funding
5. Events - Conferences, workshops, meetups

For each category:
- Execute multiple searches with different angles
- Analyze results for significance
- Note any unexpected discoveries or trends
- Save findings with your expert analysis

Return a summary of all significant findings and confirm which files were saved."""

    try:
        result = agent.invoke({"input": research_task})
        
        # Collect saved files
        output_files = []
        for fname in os.listdir(RESEARCH_DIR):
            if fname.endswith(".md"):
                output_files.append(os.path.relpath(
                    os.path.join(RESEARCH_DIR, fname), 
                    ROOT
                ))
        
        return {
            "status": "completed",
            "research_task": research_task,
            "output_files": output_files,
            "raw_output": result.get("output", ""),
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "research_task": research_task,
        }


# =============================================================================
# Presentation Synthesis Agent
# =============================================================================


def create_synthesis_agent(llm: Optional[BaseChatModel] = None) -> AgentExecutor:
    """
    Create a synthesis agent for generating presentations from research data.
    
    This agent analyzes research findings and creates compelling presentations
    that highlight key insights, trends, and significance.
    """
    from langchain_openai import ChatOpenAI
    
    if llm is None:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=0.3,
        )
    
    tools = get_research_tools()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert presentation designer specializing in AI research synthesis.

Your task is to analyze research findings and create compelling presentations that:
1. Highlight the most significant discoveries
2. Identify patterns and trends across categories
3. Connect findings to broader AI landscape implications
4. Present information in an engaging, narrative format
5. Use data visualizations where appropriate (tables, timelines)

Be critical - not all findings are equally important. Focus on what matters most.

When generating presentations:
- Start with executive summary / key highlights
- Organize by category but look for cross-category themes
- Include specific examples and evidence
- End with implications and forward-looking insights

Use markdown formatting for the presentation output."""),
        ("human", "{input}"),
        ("assistant", "{agent_scratchpad}"),
    ])
    
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        max_execution_time=120,
    )
