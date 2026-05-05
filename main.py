# main.py

from graph.research_graph import build_graph

def run_research(topic: str) -> dict:
    graph = build_graph()

    initial_state = {
        "topic": topic,
        "search_results": [],
        "analysis": "",
        "critic_feedback": "",
        "confidence_scores": {},
        "final_report": "",
        "current_step": "starting",
        "iteration_count": 0
    }

    final_state = graph.invoke(initial_state)
    return final_state

if __name__ == "__main__":
    result = run_research("Impact of AI on Pakistan's job market")
    print(result["final_report"])