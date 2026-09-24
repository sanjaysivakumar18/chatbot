import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Gemini API
# -----------------------------
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 30px;
}

.welcome {
    text-align: center;
    padding: 40px 20px 20px 20px;
}

.welcome-icon {
    font-size: 60px;
}

.welcome-title {
    font-size: 28px;
    font-weight: 600;
    margin-top: 10px;
}

.welcome-text {
    color: #777;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("🤖 AI Chatbot")
    st.write("Your beginner-friendly AI assistant")

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main UI
# -----------------------------
st.markdown(
    '<div class="main-title">💬 AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your beginner-friendly AI learning assistant</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Welcome screen
# -----------------------------
if not st.session_state.messages:

    st.markdown("""
    <div class="welcome">
        <div class="welcome-icon">🤖</div>
        <div class="welcome-title">How can I help you today?</div>
        <div class="welcome-text">
            Ask me anything about coding, AI, ML, or general topics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("### 💡 Try asking")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("What is AI?", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "What is AI?"
            })
            st.rerun()

        if st.button("Explain Python", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "Explain Python"
            })
            st.rerun()

    with col2:
        if st.button("What is Machine Learning?", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "What is Machine Learning?"
            })
            st.rerun()

        if st.button("What is an API?", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "What is an API?"
            })
            st.rerun()

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------
# Generate response
# -----------------------------
if st.session_state.messages:

    last_message = st.session_state.messages[-1]

    if last_message["role"] == "user":

        if (
            len(st.session_state.messages) == 1
            or st.session_state.messages[-2]["role"] == "assistant"
        ):

            try:

                history = []

                for message in st.session_state.messages[:-1]:
                    history.append(
                        types.Content(
                            role="user" if message["role"] == "user" else "model",
                            parts=[
                                types.Part(
                                    text=message["content"]
                                )
                            ]
                        )
                    )

                chat = client.chats.create(
                    model="gemini-3.5-flash-lite",
                    history=history,
                    config=types.GenerateContentConfig(
                        system_instruction="""
You are a helpful AI tutor.

Rules:
- Explain concepts in simple beginner-friendly language.
- Use examples when useful.
- Avoid unnecessary complicated theory.
- Explain technical questions step by step.
"""
                    )
                )

                # Thinking indicator
                with st.chat_message("assistant"):
                    with st.spinner("🤔 Thinking..."):
                        response = chat.send_message(
                            last_message["content"]
                        )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text
                })

                st.rerun()

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# -----------------------------
# Chat input
# -----------------------------
user_message = st.chat_input("Ask me anything...")

if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    st.rerun()