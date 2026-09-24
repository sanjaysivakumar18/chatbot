import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# =========================================================
# SETUP
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# GEMINI
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# WHITE + BLUE UI
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       FORCE ENTIRE STREAMLIT PAGE TO WHITE
       ===================================================== */

    html {
        background-color: #ffffff !important;
    }

    body {
        background-color: #ffffff !important;
        margin: 0 !important;
    }

    #root {
        background-color: #ffffff !important;
    }

    .stApp {
        background-color: #ffffff !important;
        min-height: 100vh !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        min-height: 100vh !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background-color: #ffffff !important;
        min-height: 100vh !important;
    }

    [data-testid="stMain"] {
        background-color: #ffffff !important;
    }

    /* =====================================================
       TOP AREA
       ===================================================== */

    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        background: #ffffff !important;
    }

    /* =====================================================
       BOTTOM AREA
       ===================================================== */

    footer {
        display: none !important;
        background-color: #ffffff !important;
    }

    [data-testid="stBottom"] {
        background-color: #ffffff !important;
    }

    [data-testid="stBottomBlockContainer"] {
        background-color: #ffffff !important;
    }

    /* =====================================================
       MAIN CONTAINER
       ===================================================== */

    .block-container {
        max-width: 1050px !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        background-color: #ffffff !important;
    }

    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background-color: #f5f9ff !important;
        border-right: 1px solid #dbeafe !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #f5f9ff !important;
    }

    /* =====================================================
       HEADINGS
       ===================================================== */

    h1 {
        color: #0f3d91 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #174ea6 !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #2563eb !important;
        font-weight: 700 !important;
    }

    /* =====================================================
       TEXT
       ===================================================== */

    p {
        color: #475569 !important;
    }

    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        width: 100% !important;
        min-height: 50px !important;

        background-color: #ffffff !important;
        color: #174ea6 !important;

        border: 1px solid #bfdbfe !important;
        border-radius: 12px !important;

        font-weight: 600 !important;
        font-size: 15px !important;

        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.06) !important;
    }

    .stButton > button:hover {
        background-color: #eff6ff !important;
        border-color: #2563eb !important;
        color: #1d4ed8 !important;

        box-shadow: 0 8px 22px rgba(37, 99, 235, 0.12) !important;
    }

    /* =====================================================
       CHAT MESSAGES
       ===================================================== */

    [data-testid="stChatMessage"] {
        background-color: #f8fbff !important;
        border: 1px solid #dbeafe !important;
        border-radius: 16px !important;

        padding: 12px 16px !important;
        margin-bottom: 12px !important;

        box-shadow: 0 3px 12px rgba(37, 99, 235, 0.04) !important;
    }

    /* =====================================================
       CHAT INPUT AREA
       ===================================================== */

    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border: 2px solid #bfdbfe !important;
        border-radius: 16px !important;

        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.08) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px #dbeafe !important;
    }

    /* =====================================================
       CHAT INPUT PARENT
       ===================================================== */

    [data-testid="stBottomBlockContainer"] {
        border-top: none !important;
        box-shadow: none !important;
    }

    /* =====================================================
       INFO BOX
       ===================================================== */

    [data-testid="stAlert"] {
        background-color: #eff6ff !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 14px !important;
    }

    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border-color: #dbeafe !important;
    }

    /* =====================================================
       SIDEBAR BUTTONS
       ===================================================== */

    [data-testid="stSidebar"] .stButton > button {
        background-color: #ffffff !important;
        border: 1px solid #dbeafe !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #eff6ff !important;
        border-color: #2563eb !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 AI Chatbot")

    st.caption("Your intelligent learning assistant")

    st.divider()

    if st.button("➕  New Conversation"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑️  Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Workspace")

    st.write(
        "Learn concepts, explore ideas, "
        "ask questions and solve problems "
        "with your AI assistant."
    )

    st.divider()

    st.subheader("Built With")

    st.write("🐍 Python")
    st.write("⚡ Streamlit")
    st.write("✦ Google Gemini")

    st.divider()

    st.caption("30 Days Grind • Day 1")

# =========================================================
# MAIN HEADER
# =========================================================

st.caption("✦  AI LEARNING ASSISTANT")

st.title("Ask. Learn. Build.")

st.write(
    "Your personal AI assistant for learning, "
    "exploration and problem solving."
)

st.divider()

# =========================================================
# WELCOME SCREEN
# =========================================================

if not st.session_state.messages:

    st.write("## 👋 Welcome")

    st.write("### What would you like to learn?")

    st.info(
        "Ask anything. Get clear explanations, "
        "examples and step-by-step guidance "
        "from your AI learning assistant."
    )

    st.write("### 💡 Suggested prompts")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🧠  What is Artificial Intelligence?"):

            st.session_state.messages.append({
                "role": "user",
                "content": "What is Artificial Intelligence?"
            })

            st.rerun()

        if st.button("🐍  Explain Python"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Explain Python in simple words."
            })

            st.rerun()

    with col2:

        if st.button("⚙️  What is Machine Learning?"):

            st.session_state.messages.append({
                "role": "user",
                "content": "What is Machine Learning?"
            })

            st.rerun()

        if st.button("🔗  What is an API?"):

            st.session_state.messages.append({
                "role": "user",
                "content": "What is an API?"
            })

            st.rerun()

# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# =========================================================
# AI RESPONSE
# =========================================================

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
                            role=(
                                "user"
                                if message["role"] == "user"
                                else "model"
                            ),
                            parts=[
                                types.Part(
                                    text=message["content"]
                                )
                            ]
                        )
                    )

                chat = client.chats.create(
                    model=MODEL,
                    history=history,
                    config=types.GenerateContentConfig(
                        system_instruction="""
You are a helpful AI tutor.

Your goal is to help the user learn.

Rules:

- Explain concepts in simple beginner-friendly language.
- Give practical examples when useful.
- Avoid unnecessary complicated theory.
- Explain technical topics step by step.
- Keep answers clear and organized.
- Help the user understand instead of simply giving answers.
- Remember previous conversation context.
"""
                    )
                )

                with st.chat_message("assistant"):

                    with st.spinner("✦ Thinking..."):

                        response = chat.send_message(
                            last_message["content"]
                        )

                        answer = response.text

                        st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.rerun()

            except Exception as e:

                st.error(f"Something went wrong: {e}")

# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "Ask your AI assistant anything..."
)

if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    st.rerun()