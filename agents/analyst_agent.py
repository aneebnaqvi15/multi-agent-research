# agents/analyst_agent.py

from langchain_groq import ChatGroq
from state.research_state import ResearchState
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please add it to your Space Secrets.")
    return ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        max_retries=3,
    )

def analyst_agent(state: ResearchState) -> ResearchState:
    """
    Reads:  topic, search_results
    Writes: analysis, current_step
    """
    llm = get_llm()
    topic = state["topic"]
    search_results = state["search_results"]

    # Format search results for LLM
    formatted_results = "\n\n".join([
        f"Source: {r.get('url', 'Unknown')}\n{r.get('content', '')[:500]}"
        for r in search_results[:5]
    ])

    prompt = f"""You are a senior research analyst.

Topic: {topic}

Research findings:
{formatted_results}

Your task:
1. Identify the 5 most important insights from the research
2. Find patterns and connections across sources
3. Note any contradictions between sources
4. Structure your analysis clearly with headings

Be specific. Cite which sources support each insight."""

    response = llm.invoke(prompt)

    return {
        **state,
        "analysis": response.content,
        "current_step": "analysis_complete"
    }