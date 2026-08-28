import os
from google import genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Customer Support AI Agent")
st.caption("Powered by Gemini 2.5 Flash | Instant AI Assistance")
st.divider()

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.text_input("🔑 Enter your Gemini API Key:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)

    # Store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input chat box
    if prompt := st.chat_input("Ask a question about our services..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your request..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("👋 Welcome! Please provide a Gemini API Key to start chatting with the agent.")