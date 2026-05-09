import streamlit as st
import time
import datetime
import streamlit.components.v1 as components
from chatbot import chatbot_response

st.set_page_config(page_title="Campus AI", page_icon="🎓", layout="wide")

# ===== CSS =====
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding-top: 0 !important;
}

[data-testid="stMain"] {
    padding-top: 0 !important;
}

/* ===== CONTAINER ===== */
.container {
    max-width: 760px;
    margin: auto;
    padding-bottom: 220px;
    margin-top: -200px;
    padding-top: 0;
}

/* ===== TITLE ===== */
.title {
    text-align: center;
    font-size: 60px;
    font-weight: 800;
    color: white;
    margin-top: 0;
    margin-bottom: 5px;
    padding-top: 10px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 20px;
    margin-top: 0;
}

/* ===== CHIPS ===== */
.stButton > button {
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    color: #cbd5f5;
    padding: 6px 14px;
    font-size: 13px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: rgba(99,102,241,0.2);
    box-shadow: 0 0 12px rgba(99,102,241,0.6);
}

/* ===== CHAT ===== */
.row {
    display: flex;
    width: 100%;
    align-items: center;
}

.row.user {
    justify-content: flex-end;
}

.row.bot {
    justify-content: flex-start;
}

.icon {
    display: inline-block;
    width: 18px;
    height: 18px;
    vertical-align: middle;
    background-size: contain;
    background-repeat: no-repeat;
}

.row.bot .icon {
    margin-right: 10px;
}

.row.user .icon {
    margin-left: 10px;
}

.user-icon {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='22' r='12' fill='%23ffffff'/%3E%3Cpath d='M16 60c0-10 8-18 16-18s16 8 16 18' fill='none' stroke='%23ffffff' stroke-width='5' stroke-linecap='round'/%3E%3Cpath d='M14 36c0-7 8-12 18-12s18 5 18 12' fill='none' stroke='%23ffffff' stroke-width='4' stroke-linecap='round'/%3E%3Cpath d='M20 22c0 5 4 8 4 8M44 22c0 5-4 8-4 8' fill='none' stroke='%230b1120' stroke-width='3' stroke-linecap='round'/%3E%3Cpath d='M24 38c4 4 16 4 20 0' fill='none' stroke='%230b1120' stroke-width='3'/%3E%3C/svg%3E");
}

.bot-icon {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='14' y='16' width='36' height='32' rx='6' fill='%23636cf1'/%3E%3Crect x='20' y='12' width='24' height='8' rx='4' fill='%232c3d80'/%3E%3Ccircle cx='24' cy='30' r='4' fill='%23ffffff'/%3E%3Ccircle cx='40' cy='30' r='4' fill='%23ffffff'/%3E%3Cpath d='M22 42h20' stroke='%23ffffff' stroke-width='4' stroke-linecap='round'/%3E%3Cpath d='M20 24h24' stroke='%232c3d80' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E");
}
.bubble {
    padding: 12px 16px 28px;
    border-radius: 20px;
    max-width: 70%;
    margin: 8px 0;

    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.1);

    box-shadow:
        0 4px 20px rgba(0,0,0,0.3),
        inset 0 0 10px rgba(255,255,255,0.05);

    animation: fadeIn 0.2s ease-in-out;
}

/* USER GLASS */
.user-bubble {
    background: linear-gradient(135deg, rgba(99,102,241,0.4), rgba(79,70,229,0.25));
    color: white;
    position: relative;
}

/* BOT GLASS */
.bot-bubble {
    background: rgba(255,255,255,0.05);
    color: #e2e8f0;
    position: relative;
}

/* ===== TIMESTAMP ===== */
.timestamp {
    position: absolute;
    bottom: 8px;
    right: 12px;
    font-size: 11px;
    color: rgba(255,255,255,0.6);
    font-weight: normal;
}

/* ===== FLOATING INPUT ===== */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    width: 720px;
    max-width: 92%;

    background: rgba(30,41,59,0.7);
    backdrop-filter: blur(12px);

    border-radius: 18px;
    padding: 10px;

    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    z-index: 999;
}

/* ===== ANIMATION ===== */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}

/* ===== MOBILE ===== */
@media (max-width: 768px) {
    .container { max-width: 95%; }
    .bubble { max-width: 85%; }
}

</style>
""", unsafe_allow_html=True)

# ===== UI =====
st.markdown("<div class='container'>", unsafe_allow_html=True)

st.markdown("<div class='title'>🎓 Campus AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask about admissions, courses, fees, hostels, placements, and campus services</div>", unsafe_allow_html=True)

# ===== CHIPS =====
col1, col2, col3, col4 = st.columns(4, gap="medium")

clicked = None
with col1:
    if st.button("Admission process", use_container_width=True):
        clicked = "Admission process?"
        
with col2:
    if st.button("Show fee structure", use_container_width=True):
        clicked = "Show fee structure"
        
with col3:
    if st.button("Hostel facilities", use_container_width=True):
        clicked = "Hostel facilities"
        
with col4:
    if st.button("Placement details", use_container_width=True):
        clicked = "Placement details"

# ===== SESSION =====
if "messages" not in st.session_state:
    st.session_state.messages = []

if clicked:
    timestamp = datetime.datetime.now().strftime("%H:%M")
    st.session_state.messages.append(("user", clicked, timestamp))
    st.rerun()

# ===== CHAT =====
for sender, msg, timestamp in st.session_state.messages:
    if sender == "user":
        st.markdown(f'''
        <div class="row user">
            <div class="bubble user-bubble">{msg}<span class="timestamp">{timestamp}</span></div>
            <span class="icon user-icon"></span>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="row bot">
            <span class="icon bot-icon"></span>
            <div class="bubble bot-bubble">{msg}<br><small style="color: rgba(255,255,255,0.6); font-size: 11px;">{timestamp}</small></div>
        </div>
        ''', unsafe_allow_html=True)

# ===== BOTTOM ANCHOR =====
st.markdown("<div id='bottom'></div>", unsafe_allow_html=True)

# ===== INPUT =====
user_input = st.chat_input("Ask about your college...")

if user_input:
    timestamp = datetime.datetime.now().strftime("%H:%M")
    st.session_state.messages.append(("user", user_input, timestamp))
    st.rerun()

# ===== BOT =====
if st.session_state.messages:
    last_sender, last_msg, last_timestamp = st.session_state.messages[-1]

    if last_sender == "user":
        response = chatbot_response(last_msg)

        placeholder = st.empty()
        typed = ""

        for char in response:
            typed += char
            placeholder.markdown(
                f'<div class="row bot"><div class="bubble bot-bubble">🤖 {typed}</div></div>',
                unsafe_allow_html=True
            )
            time.sleep(0.008)

        timestamp = datetime.datetime.now().strftime("%H:%M")
        st.session_state.messages.append(("bot", response, timestamp))
        st.rerun()

# ===== AUTO SCROLL =====
components.html("""
<script>
const scroll = () => {
    const el = parent.document.getElementById("bottom");
    if (el) el.scrollIntoView({behavior: "smooth"});
};
setTimeout(scroll, 200);
setTimeout(scroll, 500);
</script>
""", height=0)

st.markdown("</div>", unsafe_allow_html=True)