import re
import time
from datetime import datetime

import streamlit as st
from chains.research_chain import run_research_pipeline
from utils.logger import setup_logger

logger = setup_logger("ui.app")

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Premium dark theme styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        :root{
            --bg:#0a0d13; --surface:#12151c; --surface-hover:#171b24; --border:#1f2430;
            --text:#e7e9ee; --text-dim:#9096a3; --text-faint:#5c6373;
            --blue:#4f8cff; --blue-dim:rgba(79,140,255,0.14);
            --cyan:#34d3c9; --cyan-dim:rgba(52,211,201,0.14);
            --purple:#8b6cf6; --purple-dim:rgba(139,108,246,0.14);
            --green:#34d399; --green-dim:rgba(52,211,153,0.14);
        }
        .stApp{ background:var(--bg); }
        #MainMenu, footer{ visibility:hidden; }

        .hero-card{
            padding:2rem 2.2rem; border-radius:18px; margin-bottom:1.4rem;
            background:linear-gradient(135deg, #141824 0%, #0d1017 100%);
            border:1px solid var(--border);
        }
        .hero-eyebrow{
            display:inline-flex; align-items:center; gap:6px; font-size:12px; font-weight:700;
            color:var(--cyan); background:var(--cyan-dim); padding:5px 12px; border-radius:999px; margin-bottom:14px;
        }
        .hero-card h1{ margin:0 0 8px 0; font-size:2rem; font-weight:800; letter-spacing:-.5px; color:var(--text);}
        .hero-card p{ margin:0; color:var(--text-dim); font-size:1rem; max-width:640px; }

        .stButton>button{
            border-radius:10px; font-weight:700; border:1px solid var(--border);
            background:var(--surface); color:var(--text); transition:all .15s ease;
        }
        .stButton>button:hover{ background:var(--surface-hover); border-color:#2a3140; transform:translateY(-1px); }
        .stButton>button[kind="primary"]{
            background:linear-gradient(135deg, var(--blue), #6f6cf0); border:none; color:#fff;
            box-shadow:0 8px 20px -8px rgba(79,140,255,0.55);
        }
        .stTextInput>div>div>input{ border-radius:10px; background:var(--surface); border-color:var(--border); }

        .agent-pill-row{ display:flex; flex-wrap:wrap; gap:8px; margin:6px 0 4px; }
        .agent-pill{
            display:inline-flex; align-items:center; gap:6px; background:var(--surface); color:var(--text-dim);
            border:1px solid var(--border); border-radius:20px; padding:5px 13px; font-size:12.5px;
        }

        .step-card{
            display:flex; align-items:center; gap:12px; background:var(--surface); border:1px solid var(--border);
            border-radius:12px; padding:12px 16px; margin-bottom:8px;
        }
        .step-card.done{ border-color:rgba(52,211,153,0.4); }
        .step-icon{ font-size:18px; width:26px; text-align:center; }
        .step-text{ font-size:13.5px; color:var(--text); flex:1; }
        .step-badge{
            font-size:11px; font-weight:700; padding:3px 10px; border-radius:999px;
            background:var(--green-dim); color:#6ee7b7;
        }

        .report-card{
            background:var(--surface); padding:28px 30px; border-radius:16px; border:1px solid var(--border);
        }
        .report-meta-row{ display:flex; gap:24px; margin:14px 0 20px; flex-wrap:wrap; }
        .meta-chip{ font-size:12px; color:var(--text-faint); }
        .meta-chip b{ color:var(--text); font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Agent roster — single source of truth for sidebar + pipeline steps
# ---------------------------------------------------------------------------
AGENTS = [
    ("📋", "Planner", "Analyzing and breaking down research goals"),
    ("🔍", "Search", "Querying DuckDuckGo, Wikipedia & Arxiv"),
    ("📊", "Research", "Extracting facts and insights"),
    ("⚖️", "Fact-Checker", "Verifying data confidence & eliminating noise"),
    ("📝", "Summarizer", "Organizing structured summaries"),
    ("🧐", "Critic", "Reviewing logical gaps and suggestions"),
    ("✍️", "Writer", "Compiling the final Markdown report"),
]

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div style='display:flex;align-items:center;gap:10px;padding:4px 0 6px;'>"
        "<div style='width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#4f8cff,#8b6cf6);"
        "display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:15px;'>🔬</div>"
        "<div style='font-weight:700;font-size:16px;'>Control Center</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(f"### ⚙️ Pipeline Overview ({len(AGENTS)} agents)")
    pills = "".join(f"<span class='agent-pill'>{icon} {name}</span>" for icon, name, _ in AGENTS)
    st.markdown(f"<div class='agent-pill-row'>{pills}</div>", unsafe_allow_html=True)

    with st.expander("What each agent does"):
        for icon, name, desc in AGENTS:
            st.markdown(f"**{icon} {name}** — {desc}")

    st.markdown("---")
    st.caption("Powered by **LangChain**, **LangGraph** & Free LLM APIs (Groq / Gemini)")

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-eyebrow">✦ 7 specialized agents, one workflow</div>
        <h1>🔬 Multi-Agent AI Research System</h1>
        <p>Automated, deep-dive research driven by a collaborative multi-agent framework.
        Enter any complex topic below to trigger the full pipeline.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# ---------------------------------------------------------------------------
# Input section
# ---------------------------------------------------------------------------
with st.container(border=True):
    query = st.text_input(
        "Enter your research topic or question:",
        placeholder="e.g., Future trends and security challenges in Post-Quantum Cryptography",
    )
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        search_clicked = st.button("🚀 Start Deep Research", type="primary", use_container_width=True)
    with c2:
        clear_clicked = st.button("🗑️ Clear Results", use_container_width=True)

if clear_clicked:
    st.session_state.final_report = None
    st.session_state.last_query = ""

# ---------------------------------------------------------------------------
# Run pipeline with a premium animated step tracker
# ---------------------------------------------------------------------------
if search_clicked:
    if not query.strip():
        st.warning("⚠️ Please enter a valid research topic before starting.")
    else:
        st.markdown("#### 🤖 Multi-agent pipeline active")
        step_slots = [st.empty() for _ in AGENTS]

        def render_step(i, done):
            icon, name, desc = AGENTS[i]
            css_class = "step-card done" if done else "step-card"
            badge = "<span class='step-badge'>Done</span>" if done else ""
            step_slots[i].markdown(
                f"<div class='{css_class}'><div class='step-icon'>{icon}</div>"
                f"<div class='step-text'><b>{name}</b> — {desc}</div>{badge}</div>",
                unsafe_allow_html=True,
            )

        for i in range(len(AGENTS)):
            render_step(i, done=False)
            time.sleep(0.35)
            render_step(i, done=True)

        try:
            report = run_research_pipeline(query)
            st.session_state.final_report = report
            st.session_state.last_query = query
            st.success("✅ Research completed successfully!")
        except Exception as e:
            logger.error(f"Error during UI pipeline execution: {e}")
            st.error(f"An error occurred during execution: {str(e)}")
            st.session_state.final_report = None

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if st.session_state.final_report:
    st.balloons()
    st.markdown("---")

    res_col1, res_col2 = st.columns([3, 1])
    with res_col1:
        st.subheader("📄 Final Research Report")
    with res_col2:
        safe_slug = re.sub(r"[^a-z0-9_-]", "", st.session_state.last_query.lower().replace(" ", "_"))[:30] or "report"
        st.download_button(
            label="📥 Download Report",
            data=st.session_state.final_report,
            file_name=f"research_report_{safe_slug}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown(
        f"""
        <div class="report-meta-row">
            <span class="meta-chip">Generated <b>{datetime.now().strftime('%b %d, %Y')}</b></span>
            <span class="meta-chip">Agents used <b>{len(AGENTS)}</b></span>
            <span class="meta-chip">Topic <b>{st.session_state.last_query[:40]}</b></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.final_report)
    st.markdown("</div>", unsafe_allow_html=True)