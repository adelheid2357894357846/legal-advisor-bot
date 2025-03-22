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

# here we define state str for langgraph
class ChatState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    question: str
    answer: str

legal_advisor_prompt = PromptTemplate(
    input_variables=["question", "history"],
    template="""
You are a helpful legal advisor. Use the conversation history below to provide context-aware, structured answers to the user's legal question. If the history contains specific details (e.g., names, events, or prior advice), incorporate them into your response where relevant. Answer concisely with clear, actionable steps, and include legal references if applicable.

**Conversation History:**
{history}

**Question:** {question}

Provide your answer in the following format:
1. **Step 1:** [Brief description of the action or legal principle involved]
2. **Step 2:** [Follow-up step, if any, with additional legal context]
3. **Step 3:** [Final action or advice to resolve the situation]

If the user asks you to recall or confirm something from the history (e.g., a name or detail), explicitly address it in your response (e.g., "The landlord's name is Mr. Smith, as noted earlier"). When referring to individuals or entities from the history, use their names or specific identifiers where possible to show continuity.

If relevant, include legal references, statutes, or frameworks (e.g., state landlord-tenant laws, implied warranty of habitability) that might apply, tailored to the context.

Finally, include a legal disclaimer: "This is general legal information and not a substitute for professional legal advice."
"""
)

# generating response in this node
def legal_advisor_node(state: ChatState) -> ChatState:
    llm = OpenAI()
    history = "\n".join([f"{msg.__class__.__name__}: {msg.content}" for msg in state["messages"]])
    prompt = legal_advisor_prompt.format(question=state["question"], history=history)
    answer = llm(prompt)
    state["answer"] = answer.strip()
    state["messages"].append(HumanMessage(content=state["question"]))
    state["messages"].append(AIMessage(content=state["answer"]))
    return state

# langgraph workflow
workflow = StateGraph(ChatState)
workflow.add_node("legal_advisor", legal_advisor_node)
workflow.set_entry_point("legal_advisor")
workflow.add_edge("legal_advisor", END)
graph = workflow.compile()

def get_legal_advice(question: str, conversation_id: str = "default") -> str:
    # Load existing history for existing coversation id or start a new one if theres none
    messages = conversation_memory.get(conversation_id, [])
    

    initial_state = ChatState(
        messages=messages,
        question=question,
        answer=""
    )
    
    result = graph.invoke(initial_state)
    
    # saving updated history in the memory
    conversation_memory[conversation_id] = result["messages"]
    
    return result["answer"]