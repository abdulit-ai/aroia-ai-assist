import streamlit as st
import google.generativeai as genai
import time
import json
from datetime import datetime
from typing import Optional

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ARIA · AI Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stApp"] {
    background: #0a0a0f !important;
    color: #e8e6f0 !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid #1e1e2e !important;
}
[data-testid="stSidebar"] * { font-family: 'Syne', sans-serif !important; }

/* ── Main container ── */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1100px !important;
}

/* ── Header ── */
.aria-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e1e2e;
}
.aria-logo {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #7c3aed, #a855f7, #06b6d4);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 24px rgba(124, 58, 237, 0.4);
}
.aria-title { font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em; }
.aria-title span { 
    background: linear-gradient(90deg, #a855f7, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.aria-subtitle { font-size: 0.78rem; color: #6b6b8a; font-family: 'DM Mono', monospace; margin-top: 2px; }

/* ── Chat container ── */
.chat-wrap {
    display: flex; flex-direction: column; gap: 1.2rem;
    margin-bottom: 1.5rem;
}

/* ── Message bubbles ── */
.msg-user, .msg-bot {
    display: flex; align-items: flex-start; gap: 14px;
    animation: fadeSlide 0.3s ease;
}
.msg-user { flex-direction: row-reverse; }

@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 36px; height: 36px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.avatar-user { background: linear-gradient(135deg, #7c3aed, #a855f7); }
.avatar-bot  { background: #1a1a2e; border: 1px solid #2e2e4a; }

.bubble {
    max-width: 72%;
    padding: 14px 18px;
    border-radius: 16px;
    font-size: 0.93rem;
    line-height: 1.65;
    font-family: 'DM Mono', monospace;
}
.bubble-user {
    background: linear-gradient(135deg, #3d1a7a, #4c1d95);
    border: 1px solid #5b21b6;
    color: #ede9fe;
    border-top-right-radius: 4px;
}
.bubble-bot {
    background: #111120;
    border: 1px solid #1e1e2e;
    color: #d4d0e8;
    border-top-left-radius: 4px;
}
.bubble-time {
    font-size: 0.67rem; color: #4a4a6a;
    font-family: 'DM Mono', monospace;
    margin-top: 6px;
    text-align: right;
}

/* ── Thinking indicator ── */
.thinking {
    display: flex; gap: 6px; align-items: center; padding: 12px 0;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #7c3aed;
    animation: pulse 1.4s infinite ease-in-out;
}
.dot:nth-child(2) { animation-delay: 0.2s; background: #a855f7; }
.dot:nth-child(3) { animation-delay: 0.4s; background: #06b6d4; }
@keyframes pulse {
    0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
    40%            { transform: scale(1.1); opacity: 1; }
}

/* ── Input area ── */
.stTextArea textarea {
    background: #111120 !important;
    border: 1px solid #2e2e4a !important;
    border-radius: 14px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 14px 18px !important;
    resize: none !important;
    transition: border-color 0.2s;
}
.stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.4rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.45) !important;
}

/* ── Sidebar elements ── */
.stSelectbox > div > div {
    background: #111120 !important;
    border: 1px solid #2e2e4a !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
}
.stSlider > div { color: #a855f7 !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #a855f7 !important;
}

/* ── Stats cards ── */
.stat-card {
    background: #111120;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
}
.stat-num { font-size: 1.6rem; font-weight: 800; color: #a855f7; }
.stat-lbl { font-size: 0.72rem; color: #6b6b8a; font-family: 'DM Mono', monospace; margin-top: 4px; }

/* ── Section label ── */
.section-label {
    font-size: 0.7rem; font-family: 'DM Mono', monospace;
    color: #4a4a6a; letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── Divider ── */
hr { border-color: #1e1e2e !important; margin: 1.5rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2e2e4a; border-radius: 4px; }

/* ── Alert boxes ── */
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "api_ready" not in st.session_state:
    st.session_state.api_ready = False
if "model" not in st.session_state:
    st.session_state.model = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ ARIA Config")
    st.markdown("---")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get your free key at aistudio.google.com",
    )

    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.api_ready = True
            st.success("✓ API Connected", icon="🟢")
        except Exception:
            st.error("Invalid API key")
            st.session_state.api_ready = False

    st.markdown("---")
    st.markdown('<p class="section-label">Model Settings</p>', unsafe_allow_html=True)

    model_choice = st.selectbox(
        "Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
        index=0,
    )

    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05,
                            help="Higher = more creative, Lower = more precise")

    max_tokens = st.slider("Max Output Tokens", 256, 4096, 1024, 128)

    st.markdown("---")
    st.markdown('<p class="section-label">System Prompt</p>', unsafe_allow_html=True)

    system_prompt = st.text_area(
        "Persona / Instructions",
        value="You are ARIA, an advanced AI assistant. Be concise, helpful, and insightful. Use structured formatting when it improves clarity.",
        height=120,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown('<p class="section-label">Session</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-num">{len(st.session_state.messages)}</div><div class="stat-lbl">Messages</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-num">{st.session_state.total_tokens}</div><div class="stat-lbl">Est. Tokens</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.rerun()

    export_data = json.dumps(
        [{"role": m["role"], "content": m["content"], "time": m["time"]}
         for m in st.session_state.messages],
        indent=2
    )
    st.download_button(
        "⬇ Export Chat (JSON)",
        data=export_data,
        file_name=f"aria_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True,
    )

# ── Main Area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="aria-header">
  <div class="aria-logo">✦</div>
  <div>
    <div class="aria-title"><span>ARIA</span></div>
    <div class="aria-subtitle">Adaptive Reasoning & Intelligence Assistant · Powered by Gemini</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Chat History ──────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0; color: #3a3a5a;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">✦</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #6b6b8a;">Ready to assist</div>
        <div style="font-size: 0.8rem; color: #3a3a5a; font-family: 'DM Mono', monospace; margin-top: 8px;">
            Configure your API key in the sidebar and start chatting
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="avatar avatar-user">👤</div>
                <div>
                    <div class="bubble bubble-user">{msg['content']}</div>
                    <div class="bubble-time">{msg['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-bot">
                <div class="avatar avatar-bot">✦</div>
                <div>
                    <div class="bubble bubble-bot">{msg['content']}</div>
                    <div class="bubble-time">{msg['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-label">Your Message</p>', unsafe_allow_html=True)

user_input = st.text_area(
    "Message",
    placeholder="Ask anything — analysis, writing, coding, reasoning...",
    height=110,
    label_visibility="collapsed",
    key="user_input",
)

col_send, col_example, _ = st.columns([1.2, 1.2, 4])

with col_send:
    send_clicked = st.button("Send ↑", use_container_width=True)

with col_example:
    example = st.selectbox(
        "Try example",
        ["", "Summarise quantum entanglement in 3 sentences", 
         "Write a Python function to reverse a linked list",
         "What are the pros & cons of microservices?",
         "Generate 5 startup ideas around AI + education"],
        label_visibility="collapsed",
    )
    if example:
        st.session_state["pending_example"] = example

# Handle example injection
if "pending_example" in st.session_state and st.session_state["pending_example"]:
    ex = st.session_state.pop("pending_example")
    user_input = ex

# ── LLM Call ──────────────────────────────────────────────────────────────────
def call_gemini(prompt: str, history: list, sys_prompt: str,
                model_name: str, temp: float, max_tok: int) -> Optional[str]:
    """Call Gemini API with conversation history."""
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=sys_prompt,
            generation_config=genai.GenerationConfig(
                temperature=temp,
                max_output_tokens=max_tok,
            ),
        )
        # Build Gemini chat history
        chat_history = []
        for m in history[:-1]:  # exclude last (current) user message
            role = "user" if m["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [m["content"]]})

        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


if (send_clicked or (user_input and user_input != "")) and user_input.strip():
    if not st.session_state.api_ready:
        st.error("Please enter your Gemini API key in the sidebar first.")
    else:
        now = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input.strip(),
            "time": now,
        })
        st.session_state.total_tokens += len(user_input.split())

        with st.spinner(""):
            st.markdown("""
            <div class="thinking">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
            """, unsafe_allow_html=True)
            response = call_gemini(
                prompt=user_input.strip(),
                history=st.session_state.messages,
                sys_prompt=system_prompt,
                model_name=model_choice,
                temp=temperature,
                max_tok=max_tokens,
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "time": datetime.now().strftime("%H:%M"),
        })
        st.session_state.total_tokens += len(response.split())
        st.rerun()
