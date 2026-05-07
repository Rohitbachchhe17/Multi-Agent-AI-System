"""
Multi-Agent System – Streamlit Web UI
Beautiful CrewAI-style dashboard
"""

import streamlit as st
import time
import json
import os

# Auto-load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from agents import Crew, MODEL

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Outfit', sans-serif; }

/* Animated gradient background */
@keyframes gradientBG {
  0% { background: linear-gradient(135deg, #0a0a1a, #0d1b2e, #0a1628); }
  50% { background: linear-gradient(135deg, #0d1b2e, #0a1628, #0a0a1a); }
  100% { background: linear-gradient(135deg, #0a1628, #0a0a1a, #0d1b2e); }
}
.stApp {
  animation: gradientBG 20s ease infinite;
  background-size: 400% 400%;
  min-height: 100vh;
  color: #e0e0ff;
}

/* Main header */
.main-header {
    text-align: center;
    padding: 2rem 0 1rem;
}
.main-header h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}
.main-header p {
    color: #cfd7ff;
    font-size: 1.2rem;
}

/* Agent cards */
.agent-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    /* remove blur for clarity */
    transition: all 0.3s ease;
}
.agent-card:hover {
    border-color: rgba(102,126,234,0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(102,126,234,0.2);
}
.agent-card h3 { color: #ffffff; }
.agent-card p { color: #e0e0ff; font-size: 0.95rem; }

/* Sidebar */
.stSidebar, .stSidebar * {
  background: linear-gradient(180deg, #1a1a2a, #0a0a1a) !important;
  color: #e0e0ff !important;
}

/* Input fields – solid dark background */
.stSidebar .stTextInput > div > div > input,
.stSidebar .stTextArea > div > div > textarea,
.stSidebar .stSelectbox > div > div {
  background: #222222 !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 8px !important;
  color: #e0e0ff !important;
  font-size: 1rem !important;
  padding: 0.5rem !important;
}

/* Buttons */
.stButton > button { font-size: 1.05rem; }

/* Metrics */
[data-testid="stMetricValue"] { color: #aaddff !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #cfd7ff !important; }

/* Text input (main area) – solid dark */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: #222222 !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 8px !important;
  color: #e0e0ff !important;
  font-size: 1rem !important;
  padding: 0.5rem !important;
}

/* Footer / markdown */
.stMarkdown p { color: #e0e0ff; }


/* Animated gradient background */
@keyframes gradientBG {
  0% { background: linear-gradient(135deg, #0a0a1a, #0d1b2e, #0a1628); }
  50% { background: linear-gradient(135deg, #0d1b2e, #0a1628, #0a0a1a); }
  100% { background: linear-gradient(135deg, #0a1628, #0a0a1a, #0d1b2e); }
}
.stApp {
  animation: gradientBG 20s ease infinite;
  background-size: 400% 400%;
  min-height: 100vh;
  color: #e0e0ff;
}

/* Main header */
.main-header {
    text-align: center;
    padding: 2rem 0 1rem;
}
.main-header h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}
.main-header p {
    color: #8892b0;
    font-size: 1.1rem;
}

/* Agent cards */
.agent-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    /* removed blur for clarity */
    transition: all 0.3s ease;
}
.agent-card:hover {
    border-color: rgba(102,126,234,0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(102,126,234,0.2);
}
.agent-card h3 { color: #ffffff; }
.agent-card p { color: #e0e0ff; }

    color: #e2e8f0;
    margin: 0 0 0.3rem;
    font-size: 1.1rem;
    font-weight: 700;
}
.agent-card p {
    color: #8892b0;
    margin: 0;
    font-size: 0.85rem;
}

/* Status badge */
.badge {
    display: inline-block;
    padding: 0.2rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-idle    { background: rgba(100,116,139,0.2); color: #94a3b8; border: 1px solid rgba(100,116,139,0.3); }
.badge-running { background: rgba(245,158,11,0.2);  color: #fbbf24; border: 1px solid rgba(245,158,11,0.4); }
.badge-done    { background: rgba(16,185,129,0.2);  color: #34d399; border: 1px solid rgba(16,185,129,0.4); }

/* Result box */
.result-box {
    background: rgba(10,10,30,0.8);
    border: 1px solid rgba(102,126,234,0.25);
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #ccd6f6;
    line-height: 1.7;
    white-space: pre-wrap;
    font-size: 0.9rem;
}

/* Phase label */
.phase-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #667eea;
    margin-bottom: 0.5rem;
}

/* Progress pipeline */
.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2rem 0;
}
.pipe-node {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
}
.pipe-arrow {
    color: #667eea;
    font-size: 1.5rem;
    margin: 0 0.3rem;
}

/* Sidebar */
.stSidebar, .stSidebar * {
  background: linear-gradient(180deg, #1a1a2a, #0a0a1a) !important;
  color: #e0e0ff !important;
}

    background: linear-gradient(180deg, #0d1b2e, #0a0a1a) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    width: 100%;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.5) !important;
}

/* Text input */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: #222222 !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 8px !important;
  color: #e0e0ff !important;
  font-size: 1rem !important;
}

.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: #222222 !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 8px !important;
  color: #e0e0ff !important;
}

/* Metric */
[data-testid="stMetricValue"] { color: #667eea !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #8892b0 !important; }

/* Divider */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* Expander */
.streamlit-expanderHeader { color: #e2e8f0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a1a; }
::-webkit-scrollbar-thumb { background: #667eea; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🤖 Multi-Agent AI System</h1>
    <p>CrewAI-Style • Research → Analysis → Writing Pipeline</p>
</div>
""", unsafe_allow_html=True)

# Pipeline visual
st.markdown("""
<div class="pipeline">
    <div class="pipe-node">📋 Plan</div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-node">⚡ Execute</div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-node">✅ Review</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 OpenRouter API Key",
        value=os.getenv("OPENROUTER_API_KEY", ""),
        type="password",
        placeholder="sk-or-v1-...",
        help="Get your key at openrouter.ai",
    )

    output_format = st.selectbox(
        "📄 Output Format",
        ["report", "blog post", "executive summary", "research paper", "presentation outline"],
    )

    st.markdown("---")
    st.markdown("### 🤖 Active Agents")

    # Agent cards
    agents = [
        ("🔍", "ResearchBot", "Gathers raw knowledge & data"),
        ("📊", "AnalystBot",  "Extracts insights & patterns"),
        ("✍️", "WriterBot",   "Crafts polished final output"),
    ]
    for icon, name, desc in agents:
        st.markdown(f"""
        <div class="agent-card">
            <h3>{icon} {name}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**Model:** `{MODEL}`")
    st.markdown("**Provider:** OpenRouter")
    st.markdown("**Pipeline:** Sequential")

# ─── Main Area ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "💡 Enter your research topic",
        placeholder="e.g. 'The impact of AI on software development in 2026'",
        label_visibility="visible",
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Launch Crew", use_container_width=True)

# ─── Example Topics ───────────────────────────────────────────────────────────
st.markdown("**Quick topics:**")
example_cols = st.columns(4)
examples = [
    "Multi-agent AI systems",
    "Quantum computing in 2026",
    "Web3 & decentralized apps",
    "AI in healthcare",
]
for i, ex in enumerate(examples):
    if example_cols[i].button(ex, key=f"ex_{i}"):
        topic = ex

st.markdown("---")

# ─── Execution ────────────────────────────────────────────────────────────────
if run_btn and topic:
    if not api_key:
        st.error("⚠️ Please enter your OpenRouter API key in the sidebar.")
        st.stop()

    # Inject key into env so get_client() in agents.py picks it up at call time
    os.environ["OPENROUTER_API_KEY"] = api_key

    crew = Crew()

    # Phase display
    phases = [
        ("🔍", "ResearchBot",  "Phase 1: RESEARCH",  "Gathering comprehensive data and key facts..."),
        ("📊", "AnalystBot",   "Phase 2: ANALYSIS",  "Analyzing patterns and generating insights..."),
        ("✍️", "WriterBot",    "Phase 3: WRITING",   "Crafting the final polished content..."),
    ]

    results = []
    phase_containers = []

    for icon, name, phase, desc in phases:
        c = st.container()
        with c:
            st.markdown(f'<div class="phase-label">{phase}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="agent-card">
                <h3>{icon} {name} &nbsp; <span class="badge badge-idle">IDLE</span></h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        phase_containers.append(c)

    # Run agents one by one with live updates
    for idx, (icon, name, phase, desc) in enumerate(phases):
        with phase_containers[idx]:
            # Update to RUNNING
            ph = st.empty()
            ph.markdown(f"""
            <div class="agent-card">
                <h3>{icon} {name} &nbsp; <span class="badge badge-running">⟳ RUNNING</span></h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

        with st.spinner(f"{icon} {name} is working..."):
            prev_context = "\n\n".join(r.output for r in results) if results else ""
            try:
                if idx == 0:
                    task = (
                        f"Research the following topic thoroughly: '{topic}'\n\n"
                        "Provide:\n1. **Overview** – What is this?\n"
                        "2. **Key Facts & Data** – Important stats/figures\n"
                        "3. **Current Trends** – What's happening now?\n"
                        "4. **Key Players/Concepts** – Who or what matters most?\n"
                        "5. **Open Questions** – What needs deeper analysis?"
                    )
                    result = crew.researcher.run(task)
                elif idx == 1:
                    task = (
                        f"Analyze the research on '{topic}':\n"
                        "1. **Key Insights** – What does the data tell us?\n"
                        "2. **Patterns & Trends**\n"
                        "3. **SWOT Analysis**\n"
                        "4. **Strategic Implications**\n"
                        "5. **Analytical Verdict** (2-3 sentences)"
                    )
                    result = crew.analyst.run(task, context=prev_context)
                else:
                    task = (
                        f"Write a polished {output_format} on '{topic}' using the research and analysis.\n"
                        "- Engaging title & intro\n"
                        "- Well-structured body\n"
                        "- Professional tone\n"
                        "- Actionable conclusion"
                    )
                    result = crew.writer.run(task, context=prev_context)
            except Exception as e:
                st.error(f"❌ **{name} failed:** {e}")
                st.info("💡 Check your API key in the sidebar or visit openrouter.ai to verify your account.")
                st.stop()

        results.append(result)

        # Update to DONE + show output
        with phase_containers[idx]:
            ph.markdown(f"""
            <div class="agent-card">
                <h3>{icon} {name} &nbsp; <span class="badge badge-done">✓ DONE</span></h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View {name} output", expanded=(idx == len(phases) - 1)):
                st.markdown(result.output)

    # ── Final Summary ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🎉 Mission Complete!")

    m1, m2, m3 = st.columns(3)
    m1.metric("🤖 Agents Used", "3")
    m2.metric("📄 Output Format", output_format.title())
    m3.metric("✅ Status", "Complete")

    # Download final output
    final_output = results[-1].output
    st.download_button(
        label="⬇️ Download Final Output",
        data=final_output,
        file_name=f"crew_output_{topic[:30].replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True,
    )

    # Download full JSON
    full_json = json.dumps([r.to_dict() for r in results], indent=2)
    st.download_button(
        label="⬇️ Download Full Report (JSON)",
        data=full_json,
        file_name="crew_full_report.json",
        mime="application/json",
        use_container_width=True,
    )

elif run_btn and not topic:
    st.warning("⚠️ Please enter a topic to research.")

# ─── Footer ───────────────────────────────────────────────────────────────────
else:
    st.info("👆 Enter a topic and your API key, then click **Launch Crew** to start the pipeline.")
    st.markdown("""
    ### How it works:
    | Phase | Agent | What it does |
    |-------|-------|-------------|
    | 1️⃣ Plan | 🔍 ResearchBot | Gathers comprehensive facts, trends, and key data |
    | 2️⃣ Execute | 📊 AnalystBot | Analyzes patterns, builds SWOT, draws insights |
    | 3️⃣ Review | ✍️ WriterBot | Synthesizes everything into polished final content |

    **Why Multi-Agent?** Each agent specializes → better quality than one monolithic prompt.
    """)
