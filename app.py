import streamlit as st
import json
import os
import time
from dotenv import load_dotenv
from architect import generate_architecture

load_dotenv()

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Software Architect",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

/* ── Variables ── */
:root {
  --bg:        #070b14;
  --bg2:       #0d1220;
  --surface:   #111827;
  --surface2:  #1a2235;
  --surface3:  #1f2a40;
  --border:    #1e2d45;
  --border2:   #2a3d5a;
  --primary:   #3b82f6;
  --primary-d: #1d4ed8;
  --secondary: #0ea5e9;
  --accent:    #10b981;
  --warn:      #f59e0b;
  --danger:    #ef4444;
  --text:      #e2e8f0;
  --text2:     #94a3b8;
  --text3:     #475569;
  --mono:      'DM Mono', monospace;
  --sans:      'Outfit', sans-serif;
  --radius:    10px;
  --shadow:    0 4px 24px rgba(0,0,0,0.4);
}

/* ── Reset ── */
.stApp { background: var(--bg); }
*, body, html, [class*="css"] { font-family: var(--sans) !important; color: var(--text); }
.stApp > header { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span { color: var(--text2) !important; }

/* ── Hero ── */
.hero {
  position: relative;
  padding: 3.5rem 0 2.5rem;
  text-align: center;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: -60px; left: 50%; transform: translateX(-50%);
  width: 600px; height: 300px;
  background: radial-gradient(ellipse, rgba(59,130,246,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(59,130,246,0.1);
  border: 1px solid rgba(59,130,246,0.3);
  border-radius: 50px;
  padding: 4px 14px;
  font-size: 0.75rem;
  font-family: var(--mono) !important;
  color: var(--primary) !important;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 1.2rem;
}
.hero h1 {
  font-size: 3.2rem;
  font-weight: 900;
  letter-spacing: -2px;
  line-height: 1;
  margin: 0 0 0.6rem;
  background: linear-gradient(135deg, #e2e8f0 30%, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero .tagline {
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--text2) !important;
  margin: 0 0 0.5rem;
}
.hero .description {
  font-size: 0.88rem;
  color: var(--text3) !important;
  max-width: 560px;
  margin: 0 auto;
  line-height: 1.7;
}

/* ── Input Card ── */
.input-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.8rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow);
  transition: border-color 0.2s;
}
.input-card:focus-within { border-color: var(--primary); }
.input-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text2) !important;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 0.6rem;
}

/* ── Quick Chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.8rem; }
.chip {
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: 50px;
  padding: 0.3rem 0.9rem;
  font-size: 0.78rem;
  color: var(--text2) !important;
  cursor: pointer;
  transition: all 0.15s;
  font-family: var(--mono) !important;
}
.chip:hover { background: var(--surface3); border-color: var(--primary); color: var(--primary) !important; }

/* ── Generate Button ── */
.stButton > button {
  background: linear-gradient(135deg, var(--primary), var(--primary-d)) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-family: var(--sans) !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  padding: 0.75rem 2rem !important;
  width: 100% !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 15px rgba(59,130,246,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(59,130,246,0.4) !important;
}

/* ── Loading Steps ── */
.loading-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 2rem;
  margin: 1.5rem 0;
}
.loading-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary) !important;
  margin-bottom: 1.5rem;
  font-family: var(--mono) !important;
}
.loading-step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.6rem 0;
  font-size: 0.88rem;
  color: var(--text3) !important;
  transition: color 0.3s;
}
.loading-step.active { color: var(--text) !important; }
.loading-step.done { color: var(--accent) !important; }
.step-icon { font-size: 1rem; min-width: 20px; text-align: center; }

/* ── Metrics Bar ── */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
}
.metric-item {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1rem;
  text-align: center;
  transition: border-color 0.2s, transform 0.2s;
}
.metric-item:hover { border-color: var(--primary); transform: translateY(-2px); }
.metric-val {
  font-size: 1.8rem;
  font-weight: 900;
  color: var(--primary) !important;
  line-height: 1;
}
.metric-lbl {
  font-size: 0.72rem;
  color: var(--text3) !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 0.3rem;
  font-family: var(--mono) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: var(--radius) !important;
  padding: 0.3rem !important;
  gap: 0.2rem !important;
  border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 7px !important;
  color: var(--text2) !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 0.5rem 1rem !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--primary) !important;
  color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding-top: 1.5rem !important;
}

/* ── Section Cards ── */
.section-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.section-card:hover {
  border-color: var(--border2);
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.section-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary) !important;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ── Badges ── */
.badge-row { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.badge {
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: 6px;
  padding: 0.25rem 0.7rem;
  font-size: 0.78rem;
  font-family: var(--mono) !important;
  color: var(--text2) !important;
}
.badge-blue { color: var(--primary) !important; border-color: rgba(59,130,246,0.3); background: rgba(59,130,246,0.08); }
.badge-green { color: var(--accent) !important; border-color: rgba(16,185,129,0.3); background: rgba(16,185,129,0.08); }
.badge-yellow { color: var(--warn) !important; border-color: rgba(245,158,11,0.3); background: rgba(245,158,11,0.08); }
.badge-cyan { color: var(--secondary) !important; border-color: rgba(14,165,233,0.3); background: rgba(14,165,233,0.08); }

/* ── Architecture Diagram ── */
.arch-diagram {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 2rem;
  margin: 1rem 0;
  font-family: var(--mono) !important;
}
.arch-node {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 4px;
}
.arch-box {
  background: var(--surface2);
  border: 1.5px solid var(--border2);
  border-radius: 8px;
  padding: 0.5rem 1.5rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text) !important;
  text-align: center;
  min-width: 160px;
  transition: all 0.2s;
}
.arch-box:hover { border-color: var(--primary); background: var(--surface3); }
.arch-box.primary-box { border-color: var(--primary); color: var(--primary) !important; background: rgba(59,130,246,0.08); }
.arch-box.accent-box { border-color: var(--accent); color: var(--accent) !important; background: rgba(16,185,129,0.08); }
.arch-box.warn-box { border-color: var(--warn); color: var(--warn) !important; background: rgba(245,158,11,0.08); }
.arch-arrow {
  color: var(--text3) !important;
  font-size: 1.2rem;
  margin: 0.3rem 0;
  line-height: 1;
}
.arch-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

/* ── API Endpoints ── */
.endpoint {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.65rem 0.8rem;
  border-radius: 7px;
  margin-bottom: 0.4rem;
  background: var(--surface2);
  border: 1px solid var(--border);
  transition: border-color 0.15s;
}
.endpoint:hover { border-color: var(--border2); }
.method-tag {
  font-family: var(--mono) !important;
  font-weight: 700;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  min-width: 52px;
  text-align: center;
}
.GET-tag  { background: rgba(16,185,129,0.15); color: #10b981 !important; }
.POST-tag { background: rgba(59,130,246,0.15); color: #3b82f6 !important; }
.PUT-tag  { background: rgba(245,158,11,0.15); color: #f59e0b !important; }
.DEL-tag  { background: rgba(239,68,68,0.15);  color: #ef4444 !important; }
.PATCH-tag{ background: rgba(14,165,233,0.15); color: #0ea5e9 !important; }
.ep-path  { font-family: var(--mono) !important; font-size: 0.85rem; flex: 1; }
.ep-desc  { font-size: 0.8rem; color: var(--text3) !important; flex: 2; }
.ep-lock  { font-size: 0.85rem; }

/* ── DB Tables ── */
.db-table {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 0.8rem;
  overflow: hidden;
}
.db-header {
  background: var(--surface3);
  padding: 0.7rem 1rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
}
.db-name { font-family: var(--mono) !important; font-weight: 700; font-size: 0.88rem; color: var(--accent) !important; }
.db-desc { font-size: 0.78rem; color: var(--text3) !important; margin-left: auto; }
.db-row {
  display: flex;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid rgba(30,45,69,0.5);
  font-size: 0.8rem;
  gap: 1rem;
}
.db-row:last-child { border-bottom: none; }
.db-col-name { font-family: var(--mono) !important; min-width: 140px; color: var(--text) !important; }
.db-col-type { font-family: var(--mono) !important; min-width: 160px; color: var(--secondary) !important; }
.db-col-desc { color: var(--text3) !important; }

/* ── Roadmap ── */
.phase {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.phase-line {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}
.phase-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
  border: 2px solid rgba(59,130,246,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 800;
  color: white !important;
  flex-shrink: 0;
  box-shadow: 0 0 12px rgba(59,130,246,0.3);
}
.phase-connector {
  width: 2px;
  flex: 1;
  background: linear-gradient(to bottom, rgba(59,130,246,0.4), transparent);
  min-height: 20px;
}
.phase-body {
  flex: 1;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.5rem;
  transition: border-color 0.2s;
}
.phase-body:hover { border-color: var(--primary); }
.phase-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem; }
.phase-meta {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.6rem;
  flex-wrap: wrap;
}
.phase-tag {
  font-family: var(--mono) !important;
  font-size: 0.72rem;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  background: var(--surface3);
  color: var(--text3) !important;
  border: 1px solid var(--border);
}
.phase-tasks { list-style: none; padding: 0; margin: 0; }
.phase-tasks li {
  font-size: 0.84rem;
  color: var(--text2) !important;
  padding: 0.25rem 0;
  border-bottom: 1px solid rgba(30,45,69,0.4);
}
.phase-tasks li::before { content: "→ "; color: var(--primary); font-weight: 700; }
.phase-deliverable {
  margin-top: 0.6rem;
  font-size: 0.82rem;
  color: var(--accent) !important;
}
.phase-deliverable::before { content: "✓ "; font-weight: 700; }

/* ── Component Cards ── */
.component-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
.comp-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  transition: all 0.2s;
}
.comp-card:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
.comp-name { font-weight: 700; color: var(--primary) !important; margin-bottom: 4px; }
.comp-type {
  display: inline-block;
  background: var(--surface3);
  border-radius: 4px;
  padding: 1px 6px;
  font-size: 0.72rem;
  font-family: var(--mono) !important;
  color: var(--text3) !important;
  margin-bottom: 6px;
}
.comp-desc { font-size: 0.83rem; color: var(--text2) !important; }
.comp-comms { font-size: 0.75rem; font-family: var(--mono) !important; color: var(--secondary) !important; margin-top: 6px; }

/* ── Security ── */
.security-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 0.65rem 0;
  border-bottom: 1px solid rgba(30,45,69,0.5);
  font-size: 0.88rem;
}
.security-icon { color: var(--accent) !important; margin-top: 1px; flex-shrink: 0; }

/* ── Flow Box ── */
.flow-box {
  background: var(--bg2);
  border: 1px solid var(--primary);
  border-radius: 10px;
  padding: 1rem 1.4rem;
  font-family: var(--mono) !important;
  font-size: 0.88rem;
  color: var(--accent) !important;
  margin: 1rem 0;
  letter-spacing: 0.3px;
}

/* ── Action Bar (after generate) ── */
.action-bar {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
  margin: 1rem 0;
  padding: 1rem 1.2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
}
.action-chip {
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: 6px;
  padding: 0.4rem 0.9rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text2) !important;
  cursor: pointer;
  transition: all 0.15s;
}
.action-chip:hover { background: rgba(59,130,246,0.1); border-color: var(--primary); color: var(--primary) !important; }

/* ── Credibility Indicators ── */
.cred-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; margin-bottom: 1.2rem; }
.cred-item {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
}
.cred-val { font-size: 1.3rem; font-weight: 800; color: var(--warn) !important; }
.cred-lbl { font-size: 0.72rem; color: var(--text3) !important; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px; font-family: var(--mono) !important; }

/* ── Download Buttons ── */
.stDownloadButton > button {
  background: var(--surface2) !important;
  color: var(--accent) !important;
  border: 1px solid rgba(16,185,129,0.4) !important;
  border-radius: var(--radius) !important;
  font-family: var(--mono) !important;
  font-size: 0.82rem !important;
  width: 100% !important;
  transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
  background: rgba(16,185,129,0.1) !important;
  border-color: var(--accent) !important;
  transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
  background: var(--surface2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.88rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus { border-color: var(--primary) !important; box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important; }
.stSelectbox > div > div { background: var(--surface2) !important; border-color: var(--border2) !important; }

/* ── Labels ── */
label { color: var(--text2) !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 1.2px !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Sidebar items ── */
.sidebar-section { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text3) !important; margin: 1.2rem 0 0.4rem; }
.provider-badge {
  border-radius: 8px;
  padding: 0.6rem 0.8rem;
  font-size: 0.78rem;
  font-family: var(--mono) !important;
  margin-bottom: 0.6rem;
  line-height: 1.5;
}
.free-badge { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.25); color: var(--accent) !important; }
.paid-badge { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25); color: var(--warn) !important; }

/* ── Success / Error ── */
.stAlert { border-radius: var(--radius) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem;">
        <div style="font-size: 1.1rem; font-weight: 800; color: #e2e8f0;">🏛️ AI Architect</div>
        <div style="font-size: 0.72rem; font-family: 'DM Mono', monospace; color: #475569; margin-top: 2px;">v2.0 · Professional Edition</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">⚙️ Configuration</div>', unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.3rem 0 0.8rem;'>", unsafe_allow_html=True)

    provider = st.selectbox("AI Provider", ["🟢 Groq (Free)", "🔵 OpenAI (Paid)"], index=0)
    provider_key = "groq" if "Groq" in provider else "openai"

    if provider_key == "groq":
        st.markdown('<div class="provider-badge free-badge">🆓 Free · Get key at console.groq.com</div>', unsafe_allow_html=True)
        model_options = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    else:
        st.markdown('<div class="provider-badge paid-badge">💳 Paid · Get key at platform.openai.com</div>', unsafe_allow_html=True)
        model_options = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="Paste your API key...",
        value=os.getenv("GROQ_API_KEY", "") if provider_key == "groq" else os.getenv("OPENAI_API_KEY", ""),
    )

    model = st.selectbox("Model", model_options, index=0)

    st.markdown("<hr style='margin: 1rem 0 0.5rem;'>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">💡 Example Ideas</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.75rem;color:#475569;margin:0.3rem 0 0.6rem;'>Click to auto-fill ↓</p>", unsafe_allow_html=True)

    examples = [
        ("🛒", "E-commerce platform with AI recommendations"),
        ("🏥", "Hospital management system"),
        ("🚗", "Ride-sharing app like Uber"),
        ("💬", "Real-time chat app with video calls"),
        ("📦", "Inventory and supply chain tracker"),
        ("🎓", "Online learning management system"),
        ("🏦", "Digital banking application"),
        ("🍕", "Food delivery platform"),
    ]

    for emoji, text in examples:
        if st.button(f"{emoji} {text}", key=text, use_container_width=True):
            st.session_state["selected_example"] = text
            st.rerun()

    st.markdown("<hr style='margin: 1rem 0 0.5rem;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#334155; line-height:1.9;">
    ⛓ LangChain Framework<br>
    🤖 LLaMA 3.3 / GPT-4o<br>
    🎨 Streamlit UI
    </div>
    """, unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Generative AI</div>
    <h1>AI Software Architect</h1>
    <p class="tagline">Design scalable system architectures in seconds using AI.</p>
    <p class="description">
        Turn a simple project idea into a complete software blueprint —
        architecture, tech stack, APIs, database schema, and development roadmap.
    </p>
</div>
""", unsafe_allow_html=True)


# ── INPUT AREA ────────────────────────────────────────────────────────────────
default_idea = st.session_state.get("selected_example", "")

st.markdown("""
<div style="font-size:0.8rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.5rem;">
    📝 Describe Your Project
</div>
""", unsafe_allow_html=True)

idea = st.text_area(
    label="Project Idea",
    value=default_idea,
    placeholder="e.g. Build a food delivery mobile app with real-time GPS tracking, multiple restaurant support, in-app payments, and a driver management dashboard...",
    height=110,
    label_visibility="collapsed",
)

# Quick suggestion chips
st.markdown("""
<div style="font-size:0.72rem; color:#475569; margin: 0.3rem 0 0.4rem; font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:1px;">Quick ideas:</div>
<div class="chip-row">
  <span class="chip">Food delivery app</span>
  <span class="chip">AI chat platform</span>
  <span class="chip">Online course system</span>
  <span class="chip">Digital banking</span>
  <span class="chip">Healthcare portal</span>
  <span class="chip">E-commerce store</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button("🚀 Generate Architecture", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ── RENDER HELPERS ────────────────────────────────────────────────────────────
def complexity_label(n_components, n_tables, n_endpoints):
    score = n_components + n_tables + n_endpoints
    if score < 15:   return "Low", "#10b981"
    elif score < 30: return "Medium", "#f59e0b"
    else:            return "High", "#ef4444"


def render_metrics(data):
    roadmap   = data.get("development_roadmap", {})
    team      = data.get("estimated_team", {})
    api_eps   = data.get("api_endpoints", {}).get("endpoints", [])
    tables    = data.get("database_schema", {}).get("tables", [])
    phases    = roadmap.get("phases", [])
    comps     = data.get("system_architecture", {}).get("components", [])
    complexity, c_color = complexity_label(len(comps), len(tables), len(api_eps))

    st.markdown(f"""
    <div class="metrics-grid">
      <div class="metric-item">
        <div class="metric-val">{len(phases)}</div>
        <div class="metric-lbl">Dev Phases</div>
      </div>
      <div class="metric-item">
        <div class="metric-val">{len(api_eps)}</div>
        <div class="metric-lbl">API Endpoints</div>
      </div>
      <div class="metric-item">
        <div class="metric-val">{len(tables)}</div>
        <div class="metric-lbl">DB Tables</div>
      </div>
      <div class="metric-item">
        <div class="metric-val" style="font-size:1.1rem;">{team.get('size','N/A')}</div>
        <div class="metric-lbl">Team Size</div>
      </div>
      <div class="metric-item">
        <div class="metric-val" style="font-size:1.1rem;color:{c_color};">{complexity}</div>
        <div class="metric-lbl">Complexity</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_overview(data):
    ov = data.get("project_overview", {})
    roadmap = data.get("development_roadmap", {})
    team = data.get("estimated_team", {})
    challenges = "".join(
        f'<div style="padding:0.4rem 0;font-size:0.86rem;color:#94a3b8;border-bottom:1px solid #1e2d45;">⚡ {c}</div>'
        for c in ov.get("key_challenges", [])
    )
    roles = "".join(f'<span class="badge badge-blue">{r}</span>' for r in team.get("roles", []))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class="section-card">
          <div class="section-title">📋 Project Overview</div>
          <p style="font-size:0.95rem;line-height:1.7;margin-bottom:1rem;color:#cbd5e1;">{ov.get('description','')}</p>
          <div class="badge-row" style="margin-bottom:0.8rem;">
            <span class="badge badge-blue">⊞ {ov.get('type','N/A')}</span>
            <span class="badge badge-cyan">⊕ Scale: {ov.get('scale','N/A')}</span>
          </div>
          <div style="font-size:0.72rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1px;margin:0.8rem 0 0.4rem;">
            Key Challenges
          </div>
          {challenges}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="section-card">
          <div class="section-title">📊 Project Stats</div>
          <div class="cred-grid" style="grid-template-columns:1fr;">
            <div class="cred-item">
              <div class="cred-val">{roadmap.get('estimated_duration','N/A')}</div>
              <div class="cred-lbl">Estimated Duration</div>
            </div>
            <div class="cred-item">
              <div class="cred-val">{team.get('size','N/A')}</div>
              <div class="cred-lbl">Team Size</div>
            </div>
          </div>
          <div style="margin-top:0.8rem;">
            <div style="font-size:0.72rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem;">Roles Needed</div>
            <div class="badge-row">{roles}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)


def render_tech_stack(data):
    ts = data.get("technology_stack", {})
    sections = [
        ("🖥️", "Frontend",       ts.get("frontend",{}),       "badge-blue"),
        ("⚙️", "Backend",        ts.get("backend",{}),         "badge-cyan"),
        ("🗄️", "Database",       ts.get("database",{}),        "badge-green"),
        ("☁️", "Infrastructure", ts.get("infrastructure",{}),  "badge-yellow"),
    ]

    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    for i, (icon, title, info, badge_class) in enumerate(sections):
        with cols[i]:
            reason = info.pop("reason", "") if isinstance(info, dict) else ""
            badges = "".join(
                f'<span class="badge {badge_class}">{k.replace("_"," ").title()}: {v}</span>'
                for k, v in info.items()
            )
            st.markdown(f"""
            <div class="section-card">
              <div class="section-title">{icon} {title}</div>
              <div class="badge-row">{badges}</div>
              {f'<p style="margin-top:0.8rem;font-size:0.8rem;color:#475569;font-style:italic;">{reason}</p>' if reason else ''}
            </div>
            """, unsafe_allow_html=True)


def render_architecture(data):
    arch = data.get("system_architecture", {})
    components = arch.get("components", [])

    # Pattern + Flow
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div class="section-card">
          <div class="section-title">🏗️ Pattern</div>
          <span class="badge badge-blue" style="font-size:0.88rem;padding:0.4rem 0.9rem;">{arch.get('pattern','N/A')}</span>
          <div style="margin-top:1rem;">
            <div style="font-size:0.72rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem;">Scalability</div>
            <p style="font-size:0.83rem;color:#94a3b8;line-height:1.6;">{arch.get('scalability_notes','')}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        flow = arch.get("data_flow", "")
        if flow:
            st.markdown(f"""
            <div class="section-card">
              <div class="section-title">⟶ Data Flow</div>
              <div class="flow-box">{flow}</div>
            </div>
            """, unsafe_allow_html=True)

    # Visual Diagram
    st.markdown("""
    <div class="section-card">
      <div class="section-title">🔷 Architecture Diagram</div>
    """, unsafe_allow_html=True)

    # Build simplified visual diagram
    nodes = [
        ("👤 User / Client", "primary-box"),
        ("🌐 API Gateway", ""),
        ("⚙️ Backend Services", "primary-box"),
        ("🗄️ Database Layer", "accent-box"),
    ]
    diagram_html = '<div class="arch-diagram"><div class="arch-node">'
    for i, (label, style) in enumerate(nodes):
        diagram_html += f'<div class="arch-box {style}">{label}</div>'
        if i < len(nodes) - 1:
            diagram_html += '<div class="arch-arrow">↓</div>'
    diagram_html += "</div></div>"
    st.markdown(diagram_html + "</div>", unsafe_allow_html=True)

    # Components grid
    if components:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1px;margin:1rem 0 0.6rem;">System Components</div>', unsafe_allow_html=True)
        comp_cols = st.columns(2)
        for i, comp in enumerate(components):
            with comp_cols[i % 2]:
                comms = ", ".join(comp.get("communicates_with", []))
                st.markdown(f"""
                <div class="comp-card">
                  <div class="comp-name">{comp.get('name','')}</div>
                  <span class="comp-type">{comp.get('type','')}</span>
                  <div class="comp-desc">{comp.get('responsibility','')}</div>
                  {f'<div class="comp-comms">↔ {comms}</div>' if comms else ''}
                </div>
                """, unsafe_allow_html=True)


def render_database(data):
    tables = data.get("database_schema", {}).get("tables", [])
    for table in tables:
        rows_html = "".join(
            f'<div class="db-row"><span class="db-col-name">{c.get("name","")}</span><span class="db-col-type">{c.get("type","")}</span><span class="db-col-desc">{c.get("description","")}</span></div>'
            for c in table.get("columns", [])
        )
        rels = " · ".join(table.get("relationships", []))
        st.markdown(f"""
        <div class="db-table">
          <div class="db-header">
            <span style="color:#10b981;">⬡</span>
            <span class="db-name">{table.get('name','').upper()}</span>
            <span class="db-desc">{table.get('description','')}</span>
          </div>
          <div style="padding:0.2rem 0;">
            <div class="db-row" style="background:#0d1220;">
              <span class="db-col-name" style="color:#334155;font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;">Column</span>
              <span class="db-col-type" style="color:#334155;font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;">Type</span>
              <span class="db-col-desc" style="color:#334155;font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;">Description</span>
            </div>
            {rows_html}
          </div>
          {f'<div style="padding:0.5rem 1rem;font-size:0.75rem;font-family:monospace;color:#475569;border-top:1px solid #1e2d45;">🔗 {rels}</div>' if rels else ''}
        </div>
        """, unsafe_allow_html=True)


def render_api(data):
    api = data.get("api_endpoints", {})
    st.markdown(f"""
    <div style="display:flex;gap:0.5rem;margin-bottom:1rem;flex-wrap:wrap;">
      <span class="badge badge-blue">Base: {api.get('base_url','/api/v1')}</span>
      <span class="badge badge-yellow">Auth: {api.get('authentication','JWT')}</span>
    </div>
    """, unsafe_allow_html=True)

    method_map = {"GET": "GET-tag", "POST": "POST-tag", "PUT": "PUT-tag", "DELETE": "DEL-tag", "PATCH": "PATCH-tag"}
    for ep in api.get("endpoints", []):
        method = ep.get("method", "GET")
        tag_class = method_map.get(method, "GET-tag")
        lock = "🔒" if ep.get("auth_required", False) else "🔓"
        st.markdown(f"""
        <div class="endpoint">
          <span class="method-tag {tag_class}">{method}</span>
          <span class="ep-path">{ep.get('path','')}</span>
          <span class="ep-desc">{ep.get('description','')}</span>
          <span class="ep-lock">{lock}</span>
        </div>
        """, unsafe_allow_html=True)


def render_roadmap(data):
    roadmap = data.get("development_roadmap", {})
    st.markdown(f"""
    <div style="display:flex;gap:0.8rem;margin-bottom:1.2rem;align-items:center;">
      <span class="badge badge-blue">⏱ {roadmap.get('estimated_duration','N/A')}</span>
      <span style="font-size:0.8rem;color:#475569;">{len(roadmap.get('phases',[]))} phases total</span>
    </div>
    """, unsafe_allow_html=True)

    for phase in roadmap.get("phases", []):
        tasks_html = "".join(f"<li>{t}</li>" for t in phase.get("tasks", []))
        st.markdown(f"""
        <div class="phase">
          <div class="phase-line">
            <div class="phase-dot">{phase.get('phase','')}</div>
            <div class="phase-connector"></div>
          </div>
          <div class="phase-body">
            <div class="phase-title">{phase.get('name','')}</div>
            <div class="phase-meta">
              <span class="phase-tag">⏳ {phase.get('duration','')}</span>
              <span class="phase-tag">🎯 {phase.get('milestone','')}</span>
            </div>
            <ul class="phase-tasks">{tasks_html}</ul>
            <div class="phase-deliverable">{phase.get('deliverable','')}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)


def render_security(data):
    items_html = "".join(
        f'<div class="security-item"><span class="security-icon">✓</span><span style="color:#94a3b8;">{item}</span></div>'
        for item in data.get("security_considerations", [])
    )
    st.markdown(f'<div class="section-card"><div class="section-title">🔐 Security Considerations</div>{items_html}</div>', unsafe_allow_html=True)


def generate_markdown_report(data, idea):
    ov = data.get("project_overview", {})
    ts = data.get("technology_stack", {})
    arch = data.get("system_architecture", {})
    api = data.get("api_endpoints", {})
    roadmap = data.get("development_roadmap", {})
    team = data.get("estimated_team", {})

    lines = [
        f"# {ov.get('name','Project')} — Architecture Report\n",
        f"**Generated by:** AI Software Architect  \n**Project Idea:** {idea}\n",
        "---\n",
        "## Project Overview\n",
        f"{ov.get('description','')}\n",
        f"- **Type:** {ov.get('type','')}\n- **Scale:** {ov.get('scale','')}\n",
        "### Key Challenges\n",
    ]
    for c in ov.get("key_challenges", []):
        lines.append(f"- {c}\n")

    lines += ["\n## Technology Stack\n"]
    for k, v in ts.items():
        lines.append(f"### {k.replace('_',' ').title()}\n")
        if isinstance(v, dict):
            for sk, sv in v.items():
                lines.append(f"- **{sk.replace('_',' ').title()}:** {sv}\n")

    lines += ["\n## System Architecture\n",
              f"**Pattern:** {arch.get('pattern','')}\n",
              f"**Data Flow:** {arch.get('data_flow','')}\n",
              f"**Scalability:** {arch.get('scalability_notes','')}\n"]

    lines += ["\n## API Endpoints\n",
              f"Base URL: `{api.get('base_url','/api/v1')}`  Auth: {api.get('authentication','JWT')}\n\n",
              "| Method | Endpoint | Description | Auth |\n",
              "|--------|----------|-------------|------|\n"]
    for ep in api.get("endpoints", []):
        lock = "✓" if ep.get("auth_required") else "✗"
        lines.append(f"| {ep.get('method','')} | `{ep.get('path','')}` | {ep.get('description','')} | {lock} |\n")

    lines += ["\n## Development Roadmap\n",
              f"**Estimated Duration:** {roadmap.get('estimated_duration','')}\n\n"]
    for ph in roadmap.get("phases", []):
        lines.append(f"### Phase {ph.get('phase')}: {ph.get('name','')}\n")
        lines.append(f"**Duration:** {ph.get('duration','')}  \n")
        for t in ph.get("tasks", []):
            lines.append(f"- {t}\n")
        lines.append(f"\n**Deliverable:** {ph.get('deliverable','')}\n\n")

    lines += ["\n## Security Considerations\n"]
    for s in data.get("security_considerations", []):
        lines.append(f"- {s}\n")

    lines += [f"\n## Team\n**Size:** {team.get('size','')}  \n**Roles:** {', '.join(team.get('roles',[]))}\n"]
    return "".join(lines)


# ── GENERATE ──────────────────────────────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.error("⚠️ Please enter your API key in the sidebar.")
    elif not idea or not idea.strip():
        st.error("⚠️ Please enter a project idea.")
    else:
        steps = [
            "🔍 Analyzing project requirements...",
            "🏗️  Designing system architecture...",
            "🛠️  Selecting technology stack...",
            "🗄️  Modeling database schema...",
            "🔌 Generating API endpoints...",
            "🗺️  Planning development roadmap...",
            "✅ Finalizing blueprint...",
        ]
        container = st.empty()
        html_steps = "".join(f'<div class="loading-step" id="step{i}">{s}</div>' for i, s in enumerate(steps))
        container.markdown(f"""
        <div class="loading-container">
          <div class="loading-title">⚡ Generating your architecture...</div>
          {html_steps}
        </div>
        """, unsafe_allow_html=True)

        try:
            result = generate_architecture(idea, api_key, provider_key, model)
            st.session_state["arch_result"] = result
            st.session_state["arch_idea"] = idea
            container.empty()
            st.success("✅ Architecture generated successfully!")
        except Exception as e:
            container.empty()
            st.error(f"❌ Error: {str(e)}")


# ── DISPLAY RESULTS ───────────────────────────────────────────────────────────
if "arch_result" in st.session_state:
    result   = st.session_state["arch_result"]
    idea_used = st.session_state.get("arch_idea", "")
    name     = result.get("project_overview", {}).get("name", "Project")

    st.markdown(f"""
    <div style="margin-bottom:0.3rem;">
      <h2 style="font-size:2rem;font-weight:900;letter-spacing:-1px;color:#e2e8f0;margin:0;">{name}</h2>
      <p style="font-family:'DM Mono',monospace;font-size:0.78rem;color:#334155;margin:0.3rem 0 0;">
        ↳ "{idea_used[:90]}{'...' if len(idea_used)>90 else ''}"
      </p>
    </div>
    """, unsafe_allow_html=True)

    render_metrics(result)

    # ── Export Actions ──
    md_report = generate_markdown_report(result, idea_used)
    json_str  = json.dumps(result, indent=2)
    project_slug = name.replace(" ", "_").lower()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.download_button("⬇️ Download JSON", data=json_str,
                           file_name=f"{project_slug}.json", mime="application/json", use_container_width=True)
    with col_b:
        st.download_button("📄 Download Report (.md)", data=md_report,
                           file_name=f"{project_slug}_report.md", mime="text/markdown", use_container_width=True)
    with col_c:
        if st.button("🔄 Generate New Architecture", use_container_width=True):
            del st.session_state["arch_result"]
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Tabs ──
    tabs = st.tabs(["📋 Overview", "🛠️ Tech Stack", "🏗️ Architecture", "🗄️ Database", "🔌 API Design", "🗺️ Roadmap", "🔐 Security"])
    with tabs[0]: render_overview(result)
    with tabs[1]: render_tech_stack(result)
    with tabs[2]: render_architecture(result)
    with tabs[3]: render_database(result)
    with tabs[4]: render_api(result)
    with tabs[5]: render_roadmap(result)
    with tabs[6]: render_security(result)


# ── EMPTY STATE ───────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center;padding:3.5rem 0;">
      <div style="font-size:3.5rem;margin-bottom:1rem;opacity:0.3;">🏛️</div>
      <div style="font-family:'DM Mono',monospace;font-size:0.85rem;color:#334155;line-height:2.2;">
        Enter your project idea &amp; click
        <strong style="color:#3b82f6;">Generate Architecture</strong>
      </div>
      <div style="display:flex;justify-content:center;flex-wrap:wrap;gap:0.6rem;margin-top:1.5rem;">
        <span class="badge badge-blue">System Architecture</span>
        <span class="badge badge-cyan">Tech Stack</span>
        <span class="badge badge-green">Database Schema</span>
        <span class="badge badge-yellow">API Endpoints</span>
        <span class="badge">Dev Roadmap</span>
        <span class="badge">Security Plan</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
