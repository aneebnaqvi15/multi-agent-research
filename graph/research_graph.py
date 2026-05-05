# graph/research_graph.py

from langgraph.graph import StateGraph, END
from state.research_state import ResearchState
from agents.research_agent import research_agent
from agents.analyst_agent import analyst_agent
from agents.critic_agent import critic_agent
from agents.writer_agent import writer_agent

def should_revise(state: ResearchState) -> str:
    """
    Router function — reads state, decides next node.
    """
    needs_revision = state["confidence_scores"].get("needs_revision", False)
    iteration_count = state["iteration_count"]

    if needs_revision and iteration_count < 2:
        return "analyst"
    return "writer"

def increment_iteration(state: ResearchState) -> ResearchState:
    """
    Orchestrator updates iteration count after each critic cycle.
    """
    return {
        **state,
        "iteration_count": state["iteration_count"] + 1
    }

def build_graph():
    graph = StateGraph(ResearchState)

    # Register all nodes
    graph.add_node("researcher", research_agent)
    graph.add_node("analyst", analyst_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("iterate", increment_iteration)
    graph.add_node("writer", writer_agent)

    # Define edges — flow between nodes
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "critic")
    graph.add_edge("critic", "iterate")

    # Conditional routing after iteration count updates
    graph.add_conditional_edges(
        "iterate",
        should_revise,
        {
            "analyst": "analyst",
            "writer": "writer"
        }
    )

    graph.add_edge("writer", END)

    return graph.compile()