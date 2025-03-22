import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


#more robust template for a legal bot (with the help of ai since im not a student of law)
legal_advisor_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a helpful legal advisor. Please answer the following legal question in a structured manner, providing concise and clear steps that the user can follow. Ensure your response includes any relevant legal references, if applicable, and make sure your advice is segmented for clarity.

**Question:** {question}

Provide your answer in the following format:
1. **Step 1:** [Brief description of the action or legal principle involved]
2. **Step 2:** [Follow-up step, if any, with additional legal context]
3. **Step 3:** [Final action or advice to resolve the situation]

Additionally, if relevant, include any legal references, statutes, or legal frameworks that might apply. 

Finally, please include a legal disclaimer: "This is general legal information and not a substitute for professional legal advice."
"""
)

# removed formatting logic
def get_legal_advice(question: str) -> str:
    llm = OpenAI()
    chain = LLMChain(llm=llm, prompt=legal_advisor_prompt)
    answer = chain.run({"question": question})
    cleaned_answer = answer.strip()
    return cleaned_answer