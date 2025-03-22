import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

legal_advisor_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a helpful legal advisor. Answer the following legal question with concise and segmented steps.
Question: {question}
"""
)

def get_legal_advice(question: str) -> str:
    llm = OpenAI()
    chain = LLMChain(llm=llm, prompt=legal_advisor_prompt)
    answer = chain.run({"question": question})
    cleaned_answer = answer.strip().replace("\n", " ").strip()
    return cleaned_answer
