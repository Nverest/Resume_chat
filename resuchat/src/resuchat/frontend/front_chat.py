import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Resume Chat",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Hide default Streamlit header/footer */
    #MainMenu {visibility: visible;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat input styling */
    .stChatInput > div {
        border-radius: 25px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Resume or Cover Letter",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload PDF or TXT files"
    )
    
    if uploaded_files:
        if st.button("Process Uploads", type="primary", use_container_width=True):
            for uploaded_file in uploaded_files:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(f"{uploaded_file.name} uploaded!")
                        st.session_state.clear()
                        st.rerun()
                    else:
                        st.error(f"Failed: {uploaded_file.name}")
                        st.rerun()
                except requests.exceptions.ConnectionError:
                    st.error("Backend not available")

    st.divider()
    st.header("Quick Questions")

    # Fetch resume sections from backend
    if "sections" not in st.session_state:
        try:
            resp = requests.get(f"{API_URL}/resume/sections", timeout=10)
            if resp.status_code == 200:
                st.session_state.sections = resp.json()
            else:
                st.session_state.sections = None
        except Exception:
            st.session_state.sections = None

    if st.session_state.sections:
        sections = st.session_state.sections
        
        category = st.selectbox("Category", ["jobs", "internships", "education", "projects", "skills"])
        items = sections.get(category, [])
        
        if items:
            selected = st.selectbox(f"Select {category}", items)
            if st.button("Ask about this", use_container_width=True):
                # Inject the question into chat
                st.session_state.messages.append({"role": "user", "content": f"Tell me about: {selected}"})
                st.rerun()

    st.divider()
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()



def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    if prompt := st.chat_input("Ask me anything about the resume..."):
        # Display user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response with streaming feel
        with st.chat_message("assistant"):
            with st.spinner("Writing..."):
                try:
                    message_history = st.session_state.messages
                    full_prompt = "\n".join(f"{m['role']}: {m['content']}" for m in message_history)
                    full_prompt += "\nuser: " + prompt
                    response = requests.post(
                        f"{API_URL}/chat/query",
                        json={"prompt": full_prompt},
                        timeout=30
                    )
                    bot_response = response.json().get("answer", str(response.json()))
                except requests.exceptions.ConnectionError:
                    bot_response = "Could not connect to the backend. Is the API running?"
                except requests.exceptions.Timeout:
                    bot_response = "The request timed out. Please try again."

            st.markdown(bot_response)

        st.session_state.messages.append({"role": "assistant", "content": bot_response})


def layout():
    # Show welcome only when chat is empty
    if not st.session_state.messages:
        st.markdown("## Resume Chat")
        st.markdown("Ask questions about the uploaded resume and I'll answer as if I were that person.")
        st.markdown("---")

    display_chat_messages()
    handle_user_input()


if __name__ == "__main__":
    init_session_state()
    layout()