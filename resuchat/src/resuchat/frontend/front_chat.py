import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL")

USER_AVATAR = "https://cdn.jsdelivr.net/gh/alohe/memojis/png/bluey_2.png"
BOT_AVATAR = "https://cdn.jsdelivr.net/gh/alohe/memojis/png/bluey_10.png"

st.set_page_config(
    page_title="Resume Chat",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: visible;}
    footer {visibility: hidden;}
    header {visibility: visible;}

    .stChatInput > div {
        border-radius: 25px;
    }

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
    if "sections" not in st.session_state:
        st.session_state.sections = None

init_session_state()

# Sidebar
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
                        st.session_state.sections = None # Refetch section
                        st.rerun()
                    else:
                        st.error(f"Failed: {uploaded_file.name}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend not available")

    st.divider()
    st.header("Resume Information")

    # Fetch resume sections from backend (only if not already fetched)
    if st.session_state.get("sections") is None:
        try:
            resp = requests.get(f"{API_URL}/resume/sections", timeout=10)
            if resp.status_code == 200:
                st.session_state.sections = resp.json()
        except Exception:
            pass

    # Display sections (outside the fetch block)
    if st.session_state.get("sections"):
        sections = st.session_state.sections
        category = st.selectbox("Category", ["jobs", "internships", "education", "projects", "skills"])
        items = sections.get(category, [])

        if items:
            selected = st.selectbox(f"Select {category}", items)

    st.divider()
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### Open App")
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://resuchat-frontend-featf9bwe4gwc3f0.swedencentral-01.azurewebsites.net/")

def display_message(role, content):
    """Display a single message with proper alignment"""
    if role == "user":
        st.markdown(
            f'<div style="display: flex; justify-content: flex-end; align-items: flex-start; gap: 10px; margin: 8px 0;">'
            f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            f'border-radius: 15px; padding: 12px 16px; color: white; max-width: 70%; display: inline-block;">'
            f'{content}</div>'
            f'<img src="{USER_AVATAR}" style="width: 40px; height: 40px; border-radius: 50%;">'
            f'</div>',
        unsafe_allow_html=True
    )
    else:
        st.markdown(
            f'<div style="display: flex; justify-content: flex-start; align-items: flex-start; gap: 10px; margin: 8px 0;">'
            f'<img src="{BOT_AVATAR}" style="width: 40px; height: 40px; border-radius: 50%;">'
            f'<div style="background: rgba(255, 255, 255, 0.1); '
            f'border-radius: 15px; padding: 12px 16px; color: #e0e0e0; max-width: 70%; display: inline-block;">'
            f'{content}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

def display_chat_messages():
    for message in st.session_state.messages:
        display_message(message["role"], message["content"])


def handle_user_input():
    if prompt := st.chat_input("Ask me anything about the resume..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Writing..."):
            try:
                # Include message history for context
                message_history = st.session_state.messages
                full_prompt = "\n".join(f"{m['role']}: {m['content']}" for m in message_history)
                full_prompt += "\nuser: " + prompt

                response = requests.post(
                    f"{API_URL}/chat/query",
                    json={"prompt": full_prompt},
                    timeout=60
                )
                if response.status_code == 200 and response.text:
                    data = response.json()
                    bot_response = data.get("answer", str(data))
                else:
                    bot_response = f"Backend error: {response.status_code}"
            except requests.exceptions.ConnectionError:
                bot_response = "Could not connect to the backend. Is the API running?"
            except requests.exceptions.Timeout:
                bot_response = "The request timed out. Please try again."
            except Exception as e:
                bot_response = f"Error: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()


def layout():
    if not st.session_state.messages:
        st.markdown("## Resume Chat")
        st.markdown("Ask questions about the uploaded resume and I'll answer as if I were that person.")
        st.markdown("---")

    display_chat_messages()
    handle_user_input()


if __name__ == "__main__":
    layout()
