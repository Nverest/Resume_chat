import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from utils.helpers import read_api_endpoint, post_api_endpoint

chat_container = st.container(height=650)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_messages():
    with chat_container:
        for message in st.session_state.messages:   
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

def handle_user_input():
    input_text = st.chat_input("Ask about the resume")
    
    if input_text:
        st.session_state.messages.append({"role": "user", "content": input_text})
        message_history = st.session_state.messages
        # Call the FastAPI backend
        full_prompt = "\n".join(f"{m['role']}: {m['content']}" for m in message_history)
        full_prompt += "\nUser: " + input_text
        payload = {"prompt": str(full_prompt)}
        response = post_api_endpoint(payload, endpoint="/chat/query")
        if response.headers.get("Content-Type") == "application/json" and response.content:
            bot_response = response.json().get("answer")
        else:
            bot_response = response.text  # fallback to raw string

        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        st.rerun()

def layout():
    display_chat_messages()
    handle_user_input()

if __name__ == "__main__":
    init_session_state()
    layout()