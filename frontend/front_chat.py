import streamlit as st
import requests

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
        
        # Call the FastAPI backend
        response = requests.post(
            "http://127.0.0.1:8000/chat/query", 
            json={"prompt": input_text}
        )
        
        bot_response = response.json()
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        st.rerun()

def layout():
    display_chat_messages()
    handle_user_input()

if __name__ == "__main__":
    init_session_state()
    layout()