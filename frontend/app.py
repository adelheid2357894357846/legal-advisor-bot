import streamlit as st
import requests

CHAT_ENDPOINT = "http://legal_advisor_backend:8000/chat"
HISTORY_ENDPOINT = "http://legal_advisor_backend:8000/chat-history"
DELETE_ENDPOINT = "http://legal_advisor_backend:8000/delete-chat"

st.title("Legal Advisor Chatbot")
st.write("Ask any legal question and get advice.")

# Initialize session state for question_input (to be able to clear it since streamlit widgets are funny and they hate being changed directly)
if "question_input" not in st.session_state:
    st.session_state.question_input = ""

def submit_question():
    question = st.session_state.question_input
    if question:
        response = requests.post(CHAT_ENDPOINT, json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("answer")
            st.write(f"**Answer:** {answer}")
        else:
            st.error("Failed to get response from the backend.")
        # After submitting, we clear the inputfield so the text input doesnt have a prompt that persists over runs 
        st.session_state.question_input = ""

# Text input for the question with an on_change callback (to clear it, yes, i had to change 3 different code blocks to just clear a widgeet in streamlit)
st.text_input("Your Question:", key="question_input", on_change=submit_question)

# chat history btn logic
if st.button("View Chat History"):
    response = requests.get(HISTORY_ENDPOINT)
    if response.status_code == 200:
        chat_history = response.json()
        if "data" in chat_history:
            for entry in chat_history["data"]:
                st.write(f"**Q:** {entry['question']}")
                st.write(f"**A:** {entry['answer']}")
                st.write(f"_Date:_ {entry['created_at']}")
                st.write("---")
        else:
            st.write("No chat history available.")
    else:
        st.error("Failed to fetch chat history.")

# Manage chat deletion (delete all chats, im still trying to figure out how to make individual chat deletion but so far the streamlit btn renderers are messy and they need to have data stored across the refreshed state)
if st.button("Delete Chat History"):
    delete_response = requests.delete(DELETE_ENDPOINT)
    if delete_response.status_code == 200:
        st.success("All chats have been deleted successfully.")
    else:
        st.error("Failed to delete chat history.")
