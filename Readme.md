# 🔬 Multi-Agent Research & Report Generator

> Orchestrates multiple specialized AI agents to autonomously research, analyze, fact-check, and produce structured professional reports with cited sources.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green) ![Groq](https://img.shields.io/badge/Groq-Llama3.3-orange) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

---

## 🧠 What This Project Demonstrates

Most AI demos make a single LLM call and call it "AI research." This project does something fundamentally different — it separates research, analysis, fact-checking, and writing into specialized agents that communicate through a shared state graph.

```
Naive approach:    prompt → LLM → output
This project:      orchestrated multi-agent pipeline with 
                   conditional routing, critic patterns, 
                   and real source verification
```

This is the architecture pattern used in production enterprise AI systems.

---

## 🏗️ Agent Architecture

```
User Input: Research Topic
                ↓
    Orchestrator (LangGraph StateGraph)
                ↓
    ┌─────────────────────────────┐
    │      Research Agent         │
    │  Tavily web search          │
    │  3 targeted queries         │
    │  Real-time sources          │
    └──────────┬──────────────────┘
               ↓
    ┌─────────────────────────────┐
    │      Analyst Agent          │
    │  Synthesizes findings       │
    │  Identifies patterns        │
    │  Flags contradictions       │
    └──────────┬──────────────────┘
               ↓
    ┌─────────────────────────────┐
    │       Critic Agent          │
    │  Cross-references claims    │
    │  against Tavily sources     │  ← actual ground truth
    │  Assigns confidence score   │
    │  Flags unsupported claims   │
    └──────────┬──────────────────┘
               ↓
    ┌─────────────────────────────────────────┐
    │         Conditional Router              │
    │  needs_revision AND iterations < 2      │
    │    → back to Analyst (max 2 cycles)     │
    │  else → Writer Agent                    │
    └──────────┬──────────────────────────────┘
               ↓
    ┌─────────────────────────────┐
    │       Writer Agent          │
    │  Structured report          │
    │  Cited sources              │
    │  Confidence score disclosed │
    └──────────┬──────────────────┘
               ↓
    Professional Report + Confidence Score
```
<img width="134" height="630" alt="architecture" src="https://github.com/user-attachments/assets/d0751d5d-0f62-456c-8ef0-e2fb3ede1958" />

---

## 🔑 Key Technical Decisions

### Why LangGraph State?
Each agent reads from and writes to a shared `ResearchState` TypedDict. No agent needs to know about other agents — they only interact with state. This makes the pipeline modular, debuggable, and extensible.

```python
class ResearchState(TypedDict):
    topic: str
    search_results: List[dict]   # Research Agent writes
    analysis: str                 # Analyst Agent writes
    critic_feedback: str          # Critic Agent writes
    confidence_scores: dict       # Critic writes, UI reads
    final_report: str             # Writer Agent writes
    current_step: str             # Orchestrator tracks
    iteration_count: int          # Prevents infinite loops
```

### Why Tavily for Critic Agent?
A naive critic agent evaluates analyst output using only LLM knowledge — which means it's one LLM instance confirming another's biases. Our Critic Agent cross-references every claim against actual Tavily search results, giving it real ground truth to check against. This is the architectural difference between a critic that finds real issues vs one that just agrees.

### Why iteration_count?
Without a cycle limit, Critic → Analyst → Critic creates an infinite loop that exhausts free-tier rate limits. The Orchestrator increments this counter as a separate node (single responsibility), and the router caps revision cycles at 2 before forcing the pipeline to the Writer Agent.

### Why separate Orchestrator node for iteration?
Mixing counter increments into the Critic Agent violates single responsibility. Each node does exactly one thing — the Critic evaluates, the iterate node increments, the router decides. This makes debugging straightforward: if routing fails, only one node is responsible.

---

## 📊 Confidence Score — What It Actually Means

```
High score (75-100): Most claims in analysis are directly 
                     supported by Tavily search results

Low score (40-65):   Topic is speculative or emerging —
                     fewer verifiable claims in sources

Example:
  Pakistan job market report → 80/100  (established research exists)
  Iran-US war economic impact → 60/100 (speculative, fewer sources)
```

**Honest limitation:** The Critic verifies logical consistency and cross-references against search results. It cannot replace domain expert fact-checking for critical decisions.

---

## 🛠️ Tech Stack

| Tool | Purpose | Why Free |
|------|---------|---------|
| LangGraph | Agent orchestration | Open source |
| Groq API | LLM inference (Llama 3.3 70B) | Free tier, fastest inference |
| Tavily API | Real-time web search | Free tier, 1000 searches/month |
| LangChain | Tool definitions | Open source |
| Streamlit | UI | Open source |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Groq API key — [console.groq.com](https://console.groq.com)
- Tavily API key — [tavily.com](https://tavily.com)

### Installation

```bash
# Clone repo
git clone https://github.com/yourusername/multi-agent-research
cd multi-agent-research

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install langgraph langchain langchain-groq tavily-python streamlit python-dotenv

# Configure environment
cp .env.example .env
# Add your API keys to .env
```

### Environment Variables

```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### Run

```bash
# Streamlit UI
streamlit run app.py

# Terminal only
python main.py
```

---

## 📁 Project Structure

```
multi_agent_research/
├── agents/
│   ├── research_agent.py      # Tavily web search (3 queries)
│   ├── analyst_agent.py       # Synthesizes findings via LLM
│   ├── critic_agent.py        # Cross-references vs sources
│   └── writer_agent.py        # Produces final report
├── graph/
│   └── research_graph.py      # LangGraph StateGraph + routing
├── state/
│   └── research_state.py      # Shared state TypedDict
├── app.py                     # Streamlit UI
├── main.py                    # Pipeline runner
├── visualize_graph.py         # Architecture diagram generator
├── .env                       # API keys (gitignored)
├── .gitignore
└── README.md
```

---

## ⚡ Performance

| Metric | Value |
|--------|-------|
| Average report time | ~30 seconds |
| Tavily searches per run | 9 (3 queries × 3 results) |
| Max revision cycles | 2 |
| Token usage per run | ~8,000-11,000 tokens |

---

## ⚠️ Known Limitations

- **Critic cannot verify all hallucinations** — it cross-references against Tavily results but cannot catch confidently stated errors absent from search results
- **Groq free tier** — 12,000 TPM limit may cause rate limiting on complex topics
- **Tavily free tier** — 1,000 searches/month; each run uses 9 searches
- **Report quality depends on search result quality** — niche or poorly documented topics produce lower confidence scores

---

## 🗺️ What I Learned

- LangGraph state management and conditional routing
- Critic pattern in multi-agent systems — and its honest limitations
- Why multi-agent genuinely outperforms single-agent for parallel specialization
- Token optimization for free-tier LLM APIs
- Separation of concerns in agent design (single responsibility per node)

---

## 🔮 Future Improvements

- Parallel agent execution (Research + Analyst simultaneously)
- Vector store memory for cross-session topic persistence  
- PDF export for reports
- Domain-specific agent personas (legal, medical, financial)
- Human-in-the-loop approval before Writer Agent runs

---
#Demo Images
<img width="932" height="576" alt="Screenshot 2026-05-05 150608" src="https://github.com/user-attachments/assets/bebf5d3e-554d-4603-afd4-cf36eca581bc" />
---
<img width="1062" height="590" alt="Screenshot 2026-05-05 150917" src="https://github.com/user-attachments/assets/ff571e1a-2ecd-4148-966c-15b6dd469f27" />
---
<img width="1366" height="2120" alt="screencapture-localhost-8501-2026-05-05-15_09_37" src="https://github.com/user-attachments/assets/d48e0daa-d02e-4e4c-a0d0-4af3e6d1bcb6" />


*Built as Project 4 of an AI Engineering portfolio. Part of a progression from model fine-tuning → RAG systems → single agents → multi-agent orchestration.*
