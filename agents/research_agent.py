# agents/research_agent.py

from tavily import TavilyClient
from state.research_state import ResearchState
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def research_agent(state: ResearchState) -> ResearchState:
    """
    Reads:  topic
    Writes: search_results, current_step
    """
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