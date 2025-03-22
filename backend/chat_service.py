import os
import openai
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage, AIMessage
from typing import TypedDict, List
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation_memory = {}

# Define state structure for LangGraph
class ChatState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    question: str
    answer: str
#updated template to be more natural numbered step format
legal_advisor_prompt = PromptTemplate(
    input_variables=["question", "history"],
    template="""
You are a helpful legal advisor. Use the conversation history below to provide context-aware, concise, and conversational answers to the user's legal question. If the history contains specific details (e.g., names, events, or prior advice), incorporate them into your response where relevant. Provide clear and actionable information, and include legal references if applicable.

**Conversation History:**
{history}

**Question:** {question}

Respond naturally, without using a numbered step format, and tailor your answer to the question and context. If the user asks you to recall or confirm something from the history (e.g., a name or detail), explicitly address it (e.g., "As we discussed earlier, the landlord’s name is Mr. Smith"). When referring to individuals or entities from the history, use their names or specific identifiers to maintain continuity.

If relevant, include legal references, statutes, or frameworks (e.g., state landlord-tenant laws, implied warranty of habitability) that might apply, tailored to the context.

End your response with: "This is general legal information and not a substitute for professional legal advice."
"""
)

# Generate response in this node
def legal_advisor_node(state: ChatState) -> ChatState:
    llm = OpenAI()
    # Format history without class names, just the content
    history = "\n".join([msg.content for msg in state["messages"]])
    prompt = legal_advisor_prompt.format(question=state["question"], history=history)
    answer = llm(prompt)
    state["answer"] = answer.strip()
    state["messages"].append(HumanMessage(content=state["question"]))
    state["messages"].append(AIMessage(content=state["answer"]))
    return state

# LangGraph workflow
workflow = StateGraph(ChatState)
workflow.add_node("legal_advisor", legal_advisor_node)
workflow.set_entry_point("legal_advisor")
workflow.add_edge("legal_advisor", END)
graph = workflow.compile()

def get_legal_advice(question: str, conversation_id: str = "default") -> str:
    # Load existing history for the conversation ID or start a new one if none exists
    messages = conversation_memory.get(conversation_id, [])
    
    initial_state = ChatState(
        messages=messages,
        question=question,
        answer=""
    )
    
    result = graph.invoke(initial_state)
    
    # Save updated history in memory
    conversation_memory[conversation_id] = result["messages"]
    
    return result["answer"]