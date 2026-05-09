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
    background: linear-gradient(135deg, #0c0a09 0%, #1e1b4b 25%, #312e81 50%, #1e1b4b 75%, #0c0a09 100%);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    background-attachment: fixed;
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
.stButton {
    display: flex;
    justify-content: center;
}

.stButton > button {
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    color: #cbd5f5;
    padding: 8px 18px;
    font-size: 13px;
    transition: 0.3s;
    width: auto;
    min-width: 160px;
    max-width: 190px;
    white-space: nowrap;
    display: inline-flex;
    justify-content: center;
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
    width: 30px;
    height: 30px;
    min-width: 30px;
    border-radius: 50%;
    background-color: rgba(255,255,255,0.12);
    background-position: center;
    background-size: 18px 18px;
    background-repeat: no-repeat;
}

.row.bot .icon {
    margin-right: 12px;
}

.row.user .icon {
    margin-left: 12px;
}

.user-icon {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%23fde68a' stroke='%23f59e0b' stroke-width='3'/%3E%3Ccircle cx='22' cy='26' r='5' fill='%23302f2f'/%3E%3Ccircle cx='42' cy='26' r='5' fill='%23302f2f'/%3E%3Cpath d='M20 38c6 8 18 8 24 0' fill='none' stroke='%23302f2f' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E");
}

.bot-icon {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='14' y='14' width='36' height='36' rx='8' fill='%23636cf1'/%3E%3Crect x='20' y='10' width='24' height='10' rx='4' fill='%233b4abe'/%3E%3Ccircle cx='26' cy='28' r='4' fill='%23ffffff'/%3E%3Ccircle cx='38' cy='28' r='4' fill='%23ffffff'/%3E%3Cpath d='M22 40h20' stroke='%23ffffff' stroke-width='4' stroke-linecap='round'/%3E%3Cpath d='M18 22h4M42 22h4' stroke='%232c3d80' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E");
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

@keyframes gradientShift {
    0% { background-position: 0% 0%; }
    25% { background-position: 100% 0%; }
    50% { background-position: 100% 100%; }
    75% { background-position: 0% 100%; }
    100% { background-position: 0% 0%; }
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
col1, col2, col3, col4, col5, col6 = st.columns([10, 1.7, 1.7, 1.7, 1.7, 10], gap="large")

clicked = None
with col2:
    if st.button("Admission process"):
        clicked = "Admission process?"
        
with col3:
    if st.button("Show fee structure"):
        clicked = "Show fee structure"
        
with col4:
    if st.button("Hostel facilities"):
        clicked = "Hostel facilities"
        
with col5:
    if st.button("Placement details"):
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