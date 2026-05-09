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
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%23f8f5ff'/%3E%3Cpath d='M20 28c0-6 5-12 12-12s12 6 12 12' fill='%23ffe0b2'/%3E%3Cpath d='M18 38c0-9 8-16 14-16s14 7 14 16c0 9-8 16-14 16S18 47 18 38z' fill='%23ffcc99'/%3E%3Ccircle cx='24' cy='36' r='4' fill='%232b3e73'/%3E%3Ccircle cx='40' cy='36' r='4' fill='%232b3e73'/%3E%3Cpath d='M22 44c4 2 12 2 18 0' stroke='%232b3e73' stroke-width='3' fill='none'/%3E%3Cpath d='M18 22c4-4 14-8 28 0' stroke='%232b3e73' stroke-width='3' fill='none'/%3E%3C/svg%3E");
}

.bot-icon {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Cpath d='M18 22h28v20a6 6 0 0 1-6 6H24a6 6 0 0 1-6-6V22z' fill='%23636cf1'/%3E%3Cpath d='M22 18h20v6H22z' fill='%233b4abe'/%3E%3Cpath d='M24 28h6v6h-6zM38 28h6v6h-6z' fill='%23ffffff'/%3E%3Cpath d='M22 38h20' fill='none' stroke='%232c3d80' stroke-width='4' stroke-linecap='round'/%3E%3Cpath d='M28 16l-4-4M40 16l4-4' fill='none' stroke='%232c3d80' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E");
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