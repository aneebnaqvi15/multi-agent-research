# agents/research_agent.py

from tavily import TavilyClient
from state.research_state import ResearchState
import os
from dotenv import load_dotenv

load_dotenv()

def get_tavily_client():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables. Please add it to your Space Secrets.")
    return TavilyClient(api_key=api_key)

def research_agent(state: ResearchState) -> ResearchState:
    """
    Reads:  topic
    Writes: search_results, current_step
    """
    client = get_tavily_client()
    topic = state["topic"]
    
    # Run 3 targeted searches on the topic
    queries = [
        f"{topic} latest statistics 2024",
        f"{topic} expert analysis report",
        f"{topic} challenges opportunities"
    ]
    
    results = []
    for query in queries:
        response = client.search(
            query=query,
            max_results=3,
            include_raw_content=False
        )
        results.extend(response["results"])
    
    return {
        **state,
        "search_results": results,
        "current_step": "research_complete"
    }