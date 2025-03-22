import streamlit as st
import requests
import time
from datetime import datetime  # Import for timestamp formatting

st.set_page_config(page_title="Legal Advisor Chatbot", layout="wide")
CHAT_ENDPOINT = "http://legal_advisor_backend:8000/chat"
HISTORY_ENDPOINT = "http://legal_advisor_backend:8000/chat-history"
DELETE_ENDPOINT = "http://legal_advisor_backend:8000/delete-chat"

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

st.title("Legal Advisor Chatbot")
st.write("Ask any legal question and get expert advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False
#added timestamps
def display_chat():
    with st.container():
        for message in st.session_state.messages:
            css_class = "user-message" if message["role"] == "user" else "assistant-message"
            with st.chat_message(message["role"]):
                timestamp = message.get("created_at")
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else "No timestamp"
                st.markdown(
                    f'<div class="chat-message {css_class}">{message["content"]}<br><small>{timestamp_str}</small></div>',
                    unsafe_allow_html=True
                )

def show_typing_indicator(placeholder):
    for _ in range(3):
        placeholder.markdown("**.**")
        time.sleep(0.3)
        placeholder.markdown("**..**")
        time.sleep(0.3)
        placeholder.markdown("**...**")
        time.sleep(0.3)
    placeholder.empty()
#updated usrmsg with timestamp
def send_message():
    question = st.session_state.user_input.strip()
    if question:
        # Add user message with current timestamp
        st.session_state.messages.append({"role": "user", "content": question, "created_at": datetime.now()})
        st.session_state.user_input = ""

        typing_placeholder = st.empty()
        with st.chat_message("assistant"):
            show_typing_indicator(typing_placeholder)
        
        try:
            response = requests.post(CHAT_ENDPOINT, json={"question": question})
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer")
                created_at = data.get("created_at")
                if created_at:
                    created_at = datetime.fromisoformat(created_at)
                else:
                    created_at = datetime.now()
                st.session_state.messages.append({"role": "assistant", "content": answer, "created_at": created_at})
            else:
                st.error("Failed to get response from the backend.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
        finally:
            typing_placeholder.empty()

def toggle_history():
    st.session_state.show_history = not st.session_state.show_history
    if st.session_state.show_history:
        load_chat_history()

def load_chat_history():
    try:
        response = requests.get(HISTORY_ENDPOINT)
        if response.status_code == 200:
            chat_history = response.json()
            with st.sidebar:
                st.subheader("Chat History")
                for entry in chat_history.get("data", []):
                    st.markdown(f"**Q:** {entry['question']}")
                    st.markdown(f"**A:** {entry['answer']}")
                    # Format the timestamp
                    created_at = datetime.fromisoformat(entry['created_at'].replace("Z", "+00:00"))  # Handle UTC
                    formatted_time = created_at.strftime("%Y-%m-%d %H:%M:%S")
                    st.markdown(f"**Time:** {formatted_time}")
                    st.markdown("---")
        else:
            st.error("Failed to fetch chat history.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

with st.container():
    display_chat()

with st.container():
    st.text_input("Your Question:", key="user_input", on_change=send_message, placeholder="Type your legal question here...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Chat History"):
            toggle_history()

    with col2:
        if st.button("Delete Chat History"):
            try:
                response = requests.delete(DELETE_ENDPOINT)
                if response.status_code == 200:
                    success_placeholder = st.empty()
                    success_placeholder.success("All chats have been deleted successfully.")
                    time.sleep(1)
                    success_placeholder.empty()
                    st.session_state.messages.clear()
                    st.session_state.show_history = False
                else:
                    st.error("Failed to delete chat history.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")