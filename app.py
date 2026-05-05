# app.py — Multi-Agent Research Generator
# Dark theme, tabbed layout, animated agent pipeline

import streamlit as st
import time
from graph.research_graph import build_graph

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchOS — Multi-Agent AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Init session state ───────────────────────────────────────────
if "running" not in st.session_state:
    st.session_state["running"] = False
if "result" not in st.session_state:
    st.session_state["result"] = None
if "error" not in st.session_state:
    st.session_state["error"] = None
if "topic_run" not in st.session_state:
    st.session_state["topic_run"] = ""

# ── Global CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080C14 !important;
    color: #E2E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(56,189,248,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(99,102,241,0.06) 0%, transparent 50%),
        #080C14 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
section.main > div { padding: 0 !important; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1200px !important; margin: 0 auto !important; }
h1, h2, h3 { font-family: 'Space Mono', monospace !important; }

.header-wrap { display:flex; align-items:center; gap:1rem; padding:2rem 0 1.5rem; border-bottom:1px solid rgba(56,189,248,0.15); margin-bottom:2rem; }
.header-icon { width:48px; height:48px; background:linear-gradient(135deg,#0EA5E9,#6366F1); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.4rem; box-shadow:0 0 24px rgba(14,165,233,0.3); }
.header-title { font-family:'Space Mono',monospace !important; font-size:1.6rem !important; font-weight:700 !important; color:#F8FAFC !important; letter-spacing:-0.02em !important; line-height:1 !important; }
.header-sub { font-size:0.8rem !important; color:#64748B !important; letter-spacing:0.08em !important; text-transform:uppercase !important; font-family:'Space Mono',monospace !important; margin-top:0.25rem !important; }

[data-testid="stTabs"] button { font-family:'Space Mono',monospace !important; font-size:0.78rem !important; letter-spacing:0.06em !important; text-transform:uppercase !important; color:#64748B !important; background:transparent !important; border:none !important; padding:0.75rem 1.5rem !important; border-bottom:2px solid transparent !important; transition:all 0.2s ease !important; }
[data-testid="stTabs"] button:hover { color:#94A3B8 !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color:#38BDF8 !important; border-bottom:2px solid #38BDF8 !important; }
[data-testid="stTabsContent"] { padding-top:2rem !important; border-top:1px solid rgba(255,255,255,0.06) !important; }

[data-testid="stTextInput"] input { background:rgba(15,23,42,0.8) !important; border:1px solid rgba(56,189,248,0.2) !important; border-radius:10px !important; color:#F1F5F9 !important; font-family:'DM Sans',sans-serif !important; font-size:1rem !important; padding:0.85rem 1.1rem !important; }
[data-testid="stTextInput"] input:focus { border-color:rgba(56,189,248,0.6) !important; box-shadow:0 0 0 3px rgba(56,189,248,0.08) !important; outline:none !important; }
[data-testid="stTextInput"] label { color:#94A3B8 !important; font-family:'Space Mono',monospace !important; font-size:0.75rem !important; letter-spacing:0.06em !important; text-transform:uppercase !important; margin-bottom:0.5rem !important; }

[data-testid="stButton"] button { background:linear-gradient(135deg,#0EA5E9,#6366F1) !important; color:white !important; border:none !important; border-radius:10px !important; font-family:'Space Mono',monospace !important; font-size:0.8rem !important; font-weight:700 !important; letter-spacing:0.06em !important; text-transform:uppercase !important; padding:0.75rem 2rem !important; transition:all 0.2s ease !important; box-shadow:0 4px 20px rgba(14,165,233,0.25) !important; }
[data-testid="stButton"] button:hover { transform:translateY(-1px) !important; box-shadow:0 8px 28px rgba(14,165,233,0.35) !important; }

.agent-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin:1.5rem 0; }
.agent-card { background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.06); border-radius:14px; padding:1.25rem; position:relative; overflow:hidden; transition:all 0.4s ease; }
.agent-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,rgba(56,189,248,0.3),transparent); opacity:0; transition:opacity 0.4s ease; }
.agent-card.active { border-color:rgba(56,189,248,0.4); background:rgba(14,165,233,0.06); box-shadow:0 0 30px rgba(14,165,233,0.1); }
.agent-card.active::before { opacity:1; }
.agent-card.done { border-color:rgba(34,197,94,0.3); background:rgba(34,197,94,0.04); }
.agent-card.done::before { background:linear-gradient(90deg,transparent,rgba(34,197,94,0.4),transparent); opacity:1; }
.agent-icon { font-size:1.5rem; margin-bottom:0.75rem; display:block; }
.agent-name { font-family:'Space Mono',monospace; font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#94A3B8; margin-bottom:0.35rem; }
.agent-card.active .agent-name { color:#38BDF8; }
.agent-card.done .agent-name { color:#4ADE80; }
.agent-desc { font-size:0.78rem; color:#475569; line-height:1.5; }
.agent-card.active .agent-desc { color:#94A3B8; }
.agent-status { display:inline-flex; align-items:center; gap:0.4rem; margin-top:0.75rem; font-size:0.7rem; font-family:'Space Mono',monospace; letter-spacing:0.05em; }
.pulse { width:6px; height:6px; border-radius:50%; background:#38BDF8; animation:pulse 1.2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.4;transform:scale(0.8);} }
.dot-done { width:6px; height:6px; border-radius:50%; background:#4ADE80; }
.dot-idle { width:6px; height:6px; border-radius:50%; background:#334155; }

.metrics-row { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin:1.5rem 0; }
.metric-card { background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.06); border-radius:14px; padding:1.25rem 1.5rem; text-align:center; }
.metric-value { font-family:'Space Mono',monospace; font-size:2rem; font-weight:700; color:#38BDF8; line-height:1; margin-bottom:0.4rem; }
.metric-label { font-size:0.72rem; color:#64748B; letter-spacing:0.08em; text-transform:uppercase; font-family:'Space Mono',monospace; }

.report-wrap { background:rgba(15,23,42,0.5); border:1px solid rgba(255,255,255,0.06); border-radius:16px; padding:2rem 2.5rem; margin-top:1.5rem; }
.report-wrap h1,.report-wrap h2,.report-wrap h3 { font-family:'Space Mono',monospace !important; color:#F1F5F9 !important; }
.report-wrap h1 { font-size:1.4rem !important; margin-bottom:1rem !important; }
.report-wrap h2 { font-size:0.85rem !important; letter-spacing:0.08em !important; text-transform:uppercase !important; color:#38BDF8 !important; margin:1.5rem 0 0.75rem !important; padding-bottom:0.5rem !important; border-bottom:1px solid rgba(56,189,248,0.15) !important; }
.report-wrap p,.report-wrap li { color:#94A3B8 !important; line-height:1.75 !important; font-size:0.92rem !important; }
.report-wrap strong { color:#CBD5E1 !important; }
.report-wrap a { color:#38BDF8 !important; }

.conf-bar-wrap { margin:1rem 0; }
.conf-bar-label { display:flex; justify-content:space-between; font-family:'Space Mono',monospace; font-size:0.72rem; color:#64748B; margin-bottom:0.4rem; letter-spacing:0.05em; text-transform:uppercase; }
.conf-bar-track { height:4px; background:rgba(255,255,255,0.06); border-radius:2px; overflow:hidden; }
.conf-bar-fill { height:100%; border-radius:2px; background:linear-gradient(90deg,#0EA5E9,#6366F1); }

[data-testid="stDownloadButton"] button { background:rgba(15,23,42,0.8) !important; border:1px solid rgba(56,189,248,0.3) !important; color:#38BDF8 !important; box-shadow:none !important; }
[data-testid="stDownloadButton"] button:hover { background:rgba(56,189,248,0.08) !important; transform:translateY(-1px) !important; }
::-webkit-scrollbar{width:6px;}::-webkit-scrollbar-track{background:#080C14;}::-webkit-scrollbar-thumb{background:#1E293B;border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <div class="header-icon">⬡</div>
    <div>
        <div class="header-title">ResearchOS</div>
        <div class="header-sub">Multi-Agent AI Research Pipeline · LangGraph + Groq + Tavily</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Agent card renderer ─────────────────────────────────────────
def render_agents(placeholder, active=None, done=None):
    done = done or []
    agents = [
        ("🔍", "Research", "Tavily web search · 3 queries"),
        ("📊", "Analyst", "Synthesizing findings"),
        ("🔎", "Critic", "Cross-referencing sources"),
        ("✍️", "Writer", "Generating report"),
    ]
    cards = ""
    for icon, name, desc in agents:
        key = name.lower()
        if key in done:
            cls, status, color = "done", '<span class="dot-done"></span> Complete', "#4ADE80"
        elif active and key == active.lower():
            cls, status, color = "active", '<span class="pulse"></span> Running', "#38BDF8"
        else:
            cls, status, color = "", '<span class="dot-idle"></span> Waiting', "#334155"
        cards += f"""
        <div class="agent-card {cls}">
            <span class="agent-icon">{icon}</span>
            <div class="agent-name">{name}</div>
            <div class="agent-desc">{desc}</div>
            <div class="agent-status" style="color:{color};">{status}</div>
        </div>"""
    placeholder.markdown(f'<div class="agent-grid">{cards}</div>', unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["⬡  Research", "◈  Pipeline", "◉  Report"])

# ══════════════════════════════════════════════════════
# TAB 1 — INPUT
# ══════════════════════════════════════════════════════
with tab1:
    st.markdown('<p style="color:#64748B;font-size:0.85rem;margin-bottom:2rem;line-height:1.7;">Enter any research topic. Four specialized agents will autonomously search the web, synthesize findings, fact-check against sources, and produce a structured report with confidence scoring.</p>', unsafe_allow_html=True)

    topic = st.text_input("Research Topic", placeholder="e.g. Impact of AI on Pakistan's job market", key="topic_input")

    st.markdown("""
    <div style="margin:0.75rem 0 1.5rem;display:flex;gap:0.5rem;flex-wrap:wrap;">
        <span style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.2);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.75rem;color:#64748B;font-family:'Space Mono',monospace;">AI impact on Pakistan jobs</span>
        <span style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.2);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.75rem;color:#64748B;font-family:'Space Mono',monospace;">Quantum computing 2025</span>
        <span style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.2);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.75rem;color:#64748B;font-family:'Space Mono',monospace;">EV market growth trends</span>
    </div>
    """, unsafe_allow_html=True)

    run_btn = st.button("⬡  Launch Pipeline", key="run_btn")

    if run_btn and topic:
        st.session_state["running"] = True
        st.session_state["result"] = None
        st.session_state["error"] = None
        st.session_state["topic_run"] = topic
        st.toast("⬡ Pipeline launched — agents initializing...", icon="🔬")
        st.markdown("""
        <div style="margin-top:1rem;padding:1rem 1.25rem;background:rgba(14,165,233,0.06);border:1px solid rgba(56,189,248,0.25);border-radius:10px;font-family:'Space Mono',monospace;font-size:0.78rem;color:#38BDF8;letter-spacing:0.05em;">
            ⬡ Pipeline launched — switch to <strong>Pipeline tab</strong> to track live progress
        </div>
        """, unsafe_allow_html=True)
    elif run_btn and not topic:
        st.warning("Enter a research topic to begin.")

    st.markdown("""
    <div style="margin-top:2.5rem;">
        <div style="font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#334155;margin-bottom:1rem;">Agent Architecture</div>
        <div class="agent-grid">
            <div class="agent-card"><span class="agent-icon">🔍</span><div class="agent-name">Research</div><div class="agent-desc">3 targeted Tavily searches · real-time web data</div></div>
            <div class="agent-card"><span class="agent-icon">📊</span><div class="agent-name">Analyst</div><div class="agent-desc">Synthesizes findings · identifies patterns</div></div>
            <div class="agent-card"><span class="agent-icon">🔎</span><div class="agent-name">Critic</div><div class="agent-desc">Cross-references claims against sources</div></div>
            <div class="agent-card"><span class="agent-icon">✍️</span><div class="agent-name">Writer</div><div class="agent-desc">Structured report · cited sources</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 2 — PIPELINE
# ══════════════════════════════════════════════════════
with tab2:

    if not st.session_state.get("running") and not st.session_state.get("result"):
        st.markdown("""
        <div style="text-align:center;padding:4rem 0;color:#334155;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">◈</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.8rem;letter-spacing:0.1em;text-transform:uppercase;">Pipeline idle — launch from Research tab</div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.get("running"):
        topic_run = st.session_state.get("topic_run", "")

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.75rem;padding:0.85rem 1.25rem;margin-bottom:1.5rem;background:rgba(14,165,233,0.06);border:1px solid rgba(56,189,248,0.25);border-radius:10px;">
            <div class="pulse" style="width:8px;height:8px;flex-shrink:0;"></div>
            <span style="font-family:'Space Mono',monospace;font-size:0.75rem;color:#38BDF8;letter-spacing:0.05em;">PIPELINE RUNNING — processing: {topic_run}</span>
        </div>
        """, unsafe_allow_html=True)

        agent_placeholder = st.empty()
        log_placeholder = st.empty()
        render_agents(agent_placeholder, active="research")

        def log(msg):
            log_placeholder.markdown(f"""
            <div style="font-family:'Space Mono',monospace;font-size:0.75rem;color:#475569;padding:0.5rem 0;border-left:2px solid #1E293B;padding-left:1rem;margin:0.25rem 0;">
                <span style="color:#38BDF8;">→</span> {msg}
            </div>""", unsafe_allow_html=True)

        try:
            log("Research Agent initializing Tavily searches...")

            graph = build_graph()
            initial_state = {
                "topic": topic_run,
                "search_results": [],
                "analysis": "",
                "critic_feedback": "",
                "confidence_scores": {},
                "final_report": "",
                "current_step": "starting",
                "iteration_count": 0
            }

            final_state = initial_state.copy()

            for event in graph.stream(initial_state):
                node_name = list(event.keys())[0]
                final_state.update(event[node_name])

                if node_name == "researcher":
                    render_agents(agent_placeholder, active="analyst", done=["research"])
                    log("Research complete — Analyst synthesizing findings...")
                elif node_name == "analyst":
                    render_agents(agent_placeholder, active="critic", done=["research", "analyst"])
                    log("Analysis complete — Critic cross-referencing sources...")
                elif node_name == "critic":
                    score = final_state.get("confidence_scores", {}).get("score", "?")
                    render_agents(agent_placeholder, active="writer", done=["research", "analyst", "critic"])
                    log(f"Critic review done (confidence: {score}/100) — Writer generating report...")
                elif node_name == "iterate":
                    itr = final_state.get("iteration_count", 0)
                    log(f"Revision cycle {itr} — sending back to Analyst for refinement...")
                    render_agents(agent_placeholder, active="analyst", done=["research"])
                elif node_name == "writer":
                    render_agents(agent_placeholder, done=["research", "analyst", "critic", "writer"])
                    log("Report complete.")

            st.session_state["result"] = final_state
            st.session_state["running"] = False

            confidence = final_state.get("confidence_scores", {}).get("score", 0)
            st.markdown(f"""
            <div class="conf-bar-wrap" style="margin-top:1.5rem;">
                <div class="conf-bar-label"><span>Confidence Score</span><span style="color:#38BDF8;">{confidence}/100</span></div>
                <div class="conf-bar-track"><div class="conf-bar-fill" style="width:{confidence}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            st.success("✅ Report ready — view in Report tab")

        except Exception as e:
            st.session_state["running"] = False
            st.session_state["error"] = str(e)
            render_agents(agent_placeholder)
            st.error(f"Pipeline failed: {e}")

    elif st.session_state.get("result"):
        result = st.session_state["result"]
        confidence = result.get("confidence_scores", {}).get("score", 0)
        agent_placeholder = st.empty()
        render_agents(agent_placeholder, done=["research", "analyst", "critic", "writer"])
        st.markdown(f"""
        <div class="conf-bar-wrap" style="margin-top:1.5rem;">
            <div class="conf-bar-label"><span>Confidence Score</span><span style="color:#38BDF8;">{confidence}/100</span></div>
            <div class="conf-bar-track"><div class="conf-bar-fill" style="width:{confidence}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)
        st.success("✅ Pipeline complete — view report in Report tab")

# ══════════════════════════════════════════════════════
# TAB 3 — REPORT
# ══════════════════════════════════════════════════════
with tab3:
    if not st.session_state.get("result"):
        st.markdown("""
        <div style="text-align:center;padding:4rem 0;color:#334155;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">◉</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.8rem;letter-spacing:0.1em;text-transform:uppercase;">No report yet — run the pipeline first</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        result = st.session_state["result"]
        confidence = result.get("confidence_scores", {}).get("score", 0)
        iterations = result.get("iteration_count", 0)
        sources = len(result.get("search_results", []))

        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-card">
                <div class="metric-value">{confidence}<span style="font-size:1rem;color:#334155;">/100</span></div>
                <div class="metric-label">Confidence Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{iterations}</div>
                <div class="metric-label">Revision Cycles</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{sources}</div>
                <div class="metric-label">Sources Searched</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="report-wrap">', unsafe_allow_html=True)
        st.markdown(result.get("final_report", "No report generated."))
        st.markdown('</div>', unsafe_allow_html=True)

        topic_run = st.session_state.get("topic_run", "report")
        st.markdown("<div style='margin-top:1.5rem;'>", unsafe_allow_html=True)
        st.download_button(
            label="↓  Download Report (.md)",
            data=result.get("final_report", ""),
            file_name=f"research_{topic_run[:30].replace(' ', '_')}.md",
            mime="text/markdown"
        )
        st.markdown("</div>", unsafe_allow_html=True)