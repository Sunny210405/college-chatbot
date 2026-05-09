import streamlit as st
import time
import streamlit.components.v1 as components
from chatbot import chatbot_response

st.set_page_config(page_title="Campus AI", page_icon="🎓", layout="wide")

# ===== CSS =====
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* ===== CONTAINER ===== */
.container {
    max-width: 760px;
    margin: auto;
    padding-bottom: 220px;
}

/* ===== TITLE ===== */
.title {
    text-align: center;
    font-size: 60px;
    font-weight: 800;
    color: white;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 25px;
}

/* ===== CHIPS ===== */
.chips {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 25px;
}

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
}

.row.user {
    justify-content: flex-end;
}

.row.bot {
    justify-content: flex-start;
}

/* ===== GLASS BUBBLE ===== */
.bubble {
    padding: 12px 16px;
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
}

/* BOT GLASS */
.bot-bubble {
    background: rgba(255,255,255,0.05);
    color: #e2e8f0;
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
st.markdown("<div class='chips'>", unsafe_allow_html=True)

clicked = None
b1 = st.button("What is the admission process?")
b2 = st.button("Show fee structure")
b3 = st.button("Hostel facilities")
b4 = st.button("Placement details")

st.markdown("</div>", unsafe_allow_html=True)

if b1:
    clicked = "What is the admission process?"
elif b2:
    clicked = "Show fee structure"
elif b3:
    clicked = "Hostel facilities"
elif b4:
    clicked = "Placement details"

# ===== SESSION =====
if "messages" not in st.session_state:
    st.session_state.messages = []

if clicked:
    st.session_state.messages.append(("user", clicked))
    st.rerun()

# ===== CHAT =====
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f'''
        <div class="row user">
            <div class="bubble user-bubble">👤 {msg}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="row bot">
            <div class="bubble bot-bubble">🤖 {msg}</div>
        </div>
        ''', unsafe_allow_html=True)

# ===== BOTTOM ANCHOR =====
st.markdown("<div id='bottom'></div>", unsafe_allow_html=True)

# ===== INPUT =====
user_input = st.chat_input("Ask about your college...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    st.rerun()

# ===== BOT =====
if st.session_state.messages:
    last_sender, last_msg = st.session_state.messages[-1]

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

        st.session_state.messages.append(("bot", response))
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