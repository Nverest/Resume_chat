import streamlit as st
import requests
from pathlib import Path
import tempfile

# Sidebar for file upload
with st.sidebar:
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Resume or Cover Letter",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload PDF or TXT files"
    )
    
    if uploaded_files:
        if st.button("Process Uploads", type="primary"):
            with st.spinner("Processing files..."):
                for uploaded_file in uploaded_files:
                    # Send file to backend for processing
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/upload",
                            files=files
                        )
                        if response.status_code == 200:
                            st.success(f"{uploaded_file.name} uploaded successfully!")
                        else:
                            st.error(f"Failed to upload {uploaded_file.name}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

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
        
        bot_response = response.json().get("answer", str(response.json()))
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        st.rerun()

def layout():
    display_chat_messages()
    handle_user_input()

if __name__ == "__main__":
    init_session_state()
    layout()