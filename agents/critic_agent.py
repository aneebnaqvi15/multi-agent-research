# agents/critic_agent.py

from langchain_groq import ChatGroq
from state.research_state import ResearchState
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    max_retries=3,
)

def critic_agent(state: ResearchState) -> ResearchState:
    """
    Reads:  analysis, search_results, iteration_count
    Writes: critic_feedback, confidence_scores, current_step
    """
    analysis = state["analysis"]
    search_results = state["search_results"]
    iteration_count = state["iteration_count"]

    # Format source material as ground truth
    source_material = "\n\n".join([
        f"Source: {r.get('url', 'Unknown')}\n{r.get('content', '')[:500]}"
        for r in search_results[:5]
    ])

    prompt = f"""You are a rigorous fact-checker and critic.

ANALYSIS TO REVIEW:
{analysis}

ACTUAL SOURCE MATERIAL (ground truth):
{source_material}

Your task — check each claim in the analysis:

1. SUPPORTED: Claims directly backed by source material
2. UNSUPPORTED: Claims not found in any source
3. CONTRADICTED: Claims that conflict with source material
4. LOGICAL ISSUES: Weak reasoning or unsupported conclusions

For each issue found, quote the exact claim and explain the problem.

End your review with:
CONFIDENCE SCORE: [0-100]
NEEDS_REVISION: [YES/NO]
REVISION_NOTES: [specific instructions for analyst if YES]

Be rigorous. Vague analysis helps no one."""

    response = llm.invoke(prompt)
    feedback = response.content

    # Parse confidence score from response
    confidence = 70  # default
    needs_revision = False

    for line in feedback.split("\n"):
        if "CONFIDENCE SCORE:" in line:
            try:
                confidence = int(''.join(filter(str.isdigit, line)))
            except:
                confidence = 70
        if "NEEDS_REVISION: YES" in line:
            needs_revision = True

    return {
        **state,
        "critic_feedback": feedback,
        "confidence_scores": {
            "score": confidence,
            "needs_revision": needs_revision,
            "iteration": iteration_count
        },
        "current_step": "critic_complete"
    }