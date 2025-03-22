import streamlit as st
import requests
# here i was stuck on a issue where i had to look up and do some research to find out that in docker containers are isolated from each other, so localhost refers to the container itself, not the host machine or other containers
CHAT_ENDPOINT = "http://legal_advisor_backend:8000/chat"
HISTORY_ENDPOINT = "http://legal_advisor_backend:8000/chat-history"
DELETE_ENDPOINT = "http://legal_advisor_backend:8000/delete-chat"


st.title("Legal Advisor Chatbot")
st.write("Ask any legal question and get advice.")
 
question = st.text_input("Your Question:")

if st.button("Ask") and question:
    response = requests.post(CHAT_ENDPOINT, json={"question": question})
    if response.status_code == 200:
        answer = response.json().get("answer")
        st.write(f"**Answer:** {answer}")
    else:
        st.error("Failed to get response from the backend.")

# View chat history  ( used OpenAI help here since im not well versed in frontend)
if st.button("View Chat History"):
    response = requests.get(HISTORY_ENDPOINT)
    if response.status_code == 200:
        chat_history = response.json()
        if chat_history:
            for entry in chat_history:
                st.write(f"**Q:** {entry['question']}")
                st.write(f"**A:** {entry['answer']}")
                st.write(f"_Date:_ {entry['created_at']}")
                st.write("---")
        else:
            st.write("No chat history available.")
    else:
        st.error("Failed to fetch chat history.")

if st.button("Delete Chat History"):
    response = requests.delete(DELETE_ENDPOINT)
    if response.status_code == 200:
        st.success("Chat history deleted successfully.")
    else:
        st.error("Failed to delete chat history.")
