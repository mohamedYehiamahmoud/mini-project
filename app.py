import streamlit as st
import requests
import json
from datetime import datetime

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Crypto Sentiment Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000"

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 50%, #0a101f 100%);
}

/* Hide default header */
header[data-testid="stHeader"] { background: transparent; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero h1 {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00c6ff, #0072ff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #8892a4;
    font-size: 1.05rem;
    margin-top: 0;
}

/* ── Card ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}

/* ── Sentiment badge ── */
.badge {
    display: inline-block;
    padding: 0.35rem 1.1rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-bullish  { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid #00ff88; }
.badge-bearish  { background: rgba(255,68,85,0.15);  color: #ff4455; border: 1px solid #ff4455; }
.badge-neutral  { background: rgba(255,215,0,0.15);  color: #ffd700; border: 1px solid #ffd700; }

/* ── Action badge ── */
.action {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    letter-spacing: 0.04em;
}
.action-buy   { background: rgba(0,255,136,0.2); color: #00ff88; }
.action-sell  { background: rgba(255,68,85,0.2);  color: #ff4455; }
.action-hold  { background: rgba(255,215,0,0.2);  color: #ffd700; }

/* ── Stat label ── */
.stat-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #5a6478;
    margin-bottom: 0.2rem;
}
.stat-value {
    font-size: 1rem;
    color: #c9d1d9;
    line-height: 1.5;
}

/* ── Confidence bar ── */
.conf-track {
    background: rgba(255,255,255,0.08);
    border-radius: 100px;
    height: 8px;
    margin-top: 0.4rem;
    overflow: hidden;
}
.conf-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    transition: width 0.6s ease;
}

/* ── History item ── */
.history-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
}
.history-input { color: #8892a4; margin-bottom: 0.3rem; }
.history-meta  { color: #5a6478; font-size: 0.75rem; }

/* ── Error card ── */
.error-card {
    background: rgba(255,68,85,0.08);
    border: 1px solid rgba(255,68,85,0.3);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    color: #ff4455;
}

/* ── Streamlit element overrides ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: #0072ff !important;
    box-shadow: 0 0 0 2px rgba(0,114,255,0.2) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #0072ff 0%, #7b2ff7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

div[data-testid="stSidebar"] {
    background: rgba(13,17,23,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def sentiment_badge(sentiment: str) -> str:
    cls = {"BULLISH": "bullish", "BEARISH": "bearish", "NEUTRAL": "neutral"}.get(
        sentiment.upper(), "neutral"
    )
    return f'<span class="badge badge-{cls}">{sentiment}</span>'


def action_badge(action: str) -> str:
    cls = {"BUY": "buy", "SELL": "sell", "HOLD": "hold"}.get(action.upper(), "hold")
    return f'<span class="action action-{cls}">{action}</span>'


def confidence_bar(value: float) -> str:
    pct = int(value * 100)
    return f"""
    <div style="margin-top:0.2rem">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
            <span class="stat-label">Confidence</span>
            <span style="font-size:0.85rem;font-weight:600;color:#c9d1d9">{pct}%</span>
        </div>
        <div class="conf-track">
            <div class="conf-fill" style="width:{pct}%"></div>
        </div>
    </div>"""


def fetch_memory():
    try:
        r = requests.get(f"{API_BASE}/memory", timeout=3)
        return r.json().get("history", []) if r.ok else []
    except Exception:
        return []


def clear_memory_api():
    try:
        requests.delete(f"{API_BASE}/memory", timeout=3)
    except Exception:
        pass


def check_api():
    try:
        r = requests.get(f"{API_BASE}/", timeout=2)
        return r.ok
    except Exception:
        return False


# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = []


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧠 Memory")

    api_ok = check_api()
    if api_ok:
        st.markdown(
            '<span style="color:#00ff88;font-size:0.85rem">● API connected</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span style="color:#ff4455;font-size:0.85rem">● API offline — run uvicorn src.main:app --reload</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    memory = fetch_memory()
    if memory:
        st.markdown(f"**{len(memory)} stored interaction(s)**")
        for item in reversed(memory):
            inp = item.get("input", "")
            out = item.get("output", {})
            s = out.get("sentiment", "?")
            a = out.get("recommended_action", "?")
            st.markdown(
                f"""<div class="history-item">
                    <div class="history-input">📝 {inp[:60]}{'…' if len(inp)>60 else ''}</div>
                    <div class="history-meta">
                        Sentiment: <strong>{s}</strong> &nbsp;|&nbsp; Action: <strong>{a}</strong>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
        if st.button("🗑️ Clear Memory"):
            clear_memory_api()
            st.rerun()
    else:
        st.markdown(
            '<p style="color:#5a6478;font-size:0.85rem">No memory yet. Run an analysis to populate context.</p>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        '<p style="color:#5a6478;font-size:0.78rem">Model: llama-3.3-70b-versatile<br>Provider: Groq<br>Memory window: last 5</p>',
        unsafe_allow_html=True,
    )

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🚀 Crypto Sentiment Intelligence</h1>
    <p>AI-powered sentiment analysis for crypto markets — structured outputs, memory & guardrails</p>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_gap, col_examples = st.columns([3, 0.2, 1.5])

with col_input:
    text_input = st.text_area(
        "Enter crypto text to analyze",
        placeholder="e.g. Bitcoin just broke ATH! Institutional buying confirmed 🚀",
        height=130,
        label_visibility="collapsed",
    )
    analyze_btn = st.button("⚡ Analyze Sentiment")

with col_examples:
    st.markdown(
        '<p style="color:#5a6478;font-size:0.8rem;margin-bottom:0.5rem">Try an example:</p>',
        unsafe_allow_html=True,
    )
    examples = [
        "Bitcoin is pumping hard!",
        "Market crash incoming 📉",
        "ETH price is stable today",
        "Massive whale dump detected",
        "Bullish breakout confirmed 🚀",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}"):
            st.session_state["prefill"] = ex
            st.rerun()

# Prefill from example click
if "prefill" in st.session_state:
    text_input = st.session_state.pop("prefill")
    analyze_btn = True

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn and text_input.strip():
    if not api_ok:
        st.markdown(
            '<div class="error-card">⚠️ Cannot reach the API. Start it with: <code>uvicorn src.main:app --reload</code></div>',
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("Analyzing with Groq LLM..."):
            try:
                response = requests.post(
                    f"{API_BASE}/analyze",
                    json={"text": text_input},
                    timeout=30,
                )
                if response.status_code == 200:
                    result = response.json()
                    ts = datetime.now().strftime("%H:%M:%S")
                    st.session_state.results.insert(
                        0, {"input": text_input, "result": result, "time": ts}
                    )
                elif response.status_code == 400:
                    detail = response.json().get("detail", "Invalid input")
                    st.markdown(
                        f'<div class="error-card">🛡️ <strong>Guardrail blocked:</strong> {detail}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    detail = response.json().get("detail", "Unknown error")
                    st.markdown(
                        f'<div class="error-card">❌ <strong>Error {response.status_code}:</strong> {detail}</div>',
                        unsafe_allow_html=True,
                    )
            except requests.exceptions.Timeout:
                st.markdown(
                    '<div class="error-card">⏱️ Request timed out. The LLM may be slow — try again.</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.markdown(
                    f'<div class="error-card">❌ Connection error: {e}</div>',
                    unsafe_allow_html=True,
                )

elif analyze_btn and not text_input.strip():
    st.warning("Please enter some text to analyze.")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<p style="color:#5a6478;font-size:0.85rem">{len(st.session_state.results)} result(s) this session</p>',
        unsafe_allow_html=True,
    )

    for entry in st.session_state.results:
        r = entry["result"]
        inp = entry["input"]
        ts = entry["time"]
        sentiment = r.get("sentiment", "NEUTRAL").upper()
        confidence = r.get("confidence", 0.0)
        reasoning = r.get("reasoning", "—")
        insight = r.get("market_insight", "—")
        action = r.get("recommended_action", "HOLD").upper()

        st.markdown(f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;margin-bottom:1rem">
                <div>
                    <div class="stat-label" style="margin-bottom:0.3rem">Input</div>
                    <div style="color:#e6edf3;font-size:0.95rem">"{inp}"</div>
                </div>
                <div style="text-align:right">
                    {sentiment_badge(sentiment)}&nbsp;&nbsp;{action_badge(action)}
                    <div class="history-meta" style="margin-top:0.4rem">{ts}</div>
                </div>
            </div>
            {confidence_bar(confidence)}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem">
                <div>
                    <div class="stat-label">Reasoning</div>
                    <div class="stat-value">{reasoning}</div>
                </div>
                <div>
                    <div class="stat-label">Market Insight</div>
                    <div class="stat-value">{insight}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🗑️ Clear session results"):
        st.session_state.results = []
        st.rerun()
