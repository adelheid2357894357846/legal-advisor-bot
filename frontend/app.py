import streamlit as st
import requests
import time

CHAT_ENDPOINT = "http://legal_advisor_backend:8000/chat"
HISTORY_ENDPOINT = "http://legal_advisor_backend:8000/chat-history"
DELETE_ENDPOINT = "http://legal_advisor_backend:8000/delete-chat"

st.set_page_config(page_title="Legal Advisor Chatbot", layout="centered")
st.title("Legal Advisor Chatbot")
st.write("Ask any legal question and get advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False

def display_chat():
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message("user" if message["role"] == "user" else "assistant"):
                st.markdown(message["content"])

def show_typing_indicator(placeholder):
    for _ in range(3):
        placeholder.markdown("**.**")
        time.sleep(0.3)
        placeholder.markdown("**..**")
        time.sleep(0.3)
        placeholder.markdown("**...**")
        time.sleep(0.3)
    placeholder.empty()

def send_message():
    question = st.session_state.user_input.strip()
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.user_input = ""

        typing_placeholder = st.empty()
        with st.chat_message("assistant"):
            show_typing_indicator(typing_placeholder)
        
        try:
            response = requests.post(CHAT_ENDPOINT, json={"question": question})
            if response.status_code == 200:
                answer = response.json().get("answer")
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Failed to get response from the backend.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
        finally:
            typing_placeholder.empty()


# upgraded history to look better and fixed bug where it was duplicating itself ( i accidentally called it 2x in my code)
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
                    st.write(f"**Q:** {entry['question']}")
                    st.write(f"**A:** {entry['answer']}")
                    st.write("---")
        else:
            st.error("Failed to fetch chat history.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

display_chat()

st.text_input("Your Question:", key="user_input", on_change=send_message)

col1, col2 = st.columns(2)
with col1:
    if st.button("View Chat History"):
        toggle_history()

with col2:
    if st.button("Delete Chat History"):
        try:
            response = requests.delete(DELETE_ENDPOINT)
            if response.status_code == 200:
                st.success("All chats have been deleted successfully.")
                st.session_state.messages.clear()
                st.session_state.show_history = False
            else:
                st.error("Failed to delete chat history.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")