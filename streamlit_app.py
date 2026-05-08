import streamlit as st
import time
from chatbot import chatbot_response

st.set_page_config(page_title="College AI Chatbot", page_icon="🎓", layout="wide")

# 🔥 FORCE FULL DARK THEME (OVERRIDES STREAMLIT LIGHT MODE)
st.markdown("""
<style>

/* ===== GLOBAL DARK THEME ===== */
html, body, [class*="css"] {
    background-color: #0f172a !important;
    color: #e5e7eb !important;
}

/* Main app background */
[data-testid="stAppViewContainer"] {
    background: #0f172a !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #020617 !important;
}

/* Header / toolbar */
[data-testid="stHeader"] {
    background: #020617 !important;
}

/* Input box */
textarea, input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
}

/* Buttons */
button {
    background-color: #4f46e5 !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Chat container */
.chat-wrapper {
    width: 60%;
    margin: auto;
}

/* Title */
.title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 25px;
}

/* Chat bubbles */
.chat {
    padding: 14px 18px;
    border-radius: 25px;
    max-width: 70%;
    margin: 8px 0;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    animation: fadeIn 0.3s ease-in-out;
}

/* User bubble */
.user {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
}

/* Bot bubble */
.bot {
    background: #1e293b;
    color: #e2e8f0;
}

/* Alignment */
.right {
    display: flex;
    justify-content: flex-end;
}

.left {
    display: flex;
    justify-content: flex-start;
}

/* Hover effect */
.chat:hover {
    transform: scale(1.03);
    transition: 0.2s;
}

/* Fade animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🎓 College AI Chatbot</div>", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

# Display messages
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f"""
        <div class='right'>
            <div class='chat user'>👤 {msg}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='left'>
            <div class='chat bot'>🤖 {msg}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input
user_input = st.chat_input("Ask about your college...")

if user_input:
    # Step 1: Add user message FIRST
    st.session_state.messages.append(("user", user_input))

    # Step 2: Immediately display updated chat (so user appears first)
    st.rerun()


# Handle bot response AFTER rerun
if st.session_state.messages:
    last_sender, last_msg = st.session_state.messages[-1]

    # If last message is from user → generate bot reply
    if last_sender == "user":
        response = chatbot_response(last_msg)

        placeholder = st.empty()
        typed = ""

        # Typing animation
        for char in response:
            typed += char
            placeholder.markdown(f"""
            <div class='left'>
                <div class='chat bot'>🤖 {typed}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.008)

        # Save final bot message
        st.session_state.messages.append(("bot", response))

        st.rerun()