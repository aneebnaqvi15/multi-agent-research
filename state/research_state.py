# state/research_state.py

from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    # User input
    topic: str
    
    # Research Agent writes here
    search_results: List[dict]
    
    # Analyst Agent writes here
    analysis: str
    
    # Critic Agent reads analysis + search_results
    # Critic Agent writes here
    critic_feedback: str
    confidence_scores: dict
    
    # Writer Agent writes here
    final_report: str
    
    # Orchestrator tracks progress here
    current_step: str
    iteration_count: int  # prevents infinite critic loops