import os
import json
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Fetch configuration variables from environment variables
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_KEY = os.getenv("AOAI_KEY")
COMPLETIONS_DEPLOYMENT_NAME = "gpt-35-turbo"
AOAI_API_VERSION = "2023-09-01-preview"

# Initialize the AzureChatOpenAI model
llm = AzureChatOpenAI(
    temperature=0,
    openai_api_version=AOAI_API_VERSION,
    azure_endpoint=AOAI_ENDPOINT,
    openai_api_key=AOAI_KEY,
    azure_deployment=COMPLETIONS_DEPLOYMENT_NAME
)

def generate_questions(patient_response, deep_questions=5, general_questions=5):
    deep_q_template = """
    You are a medical AI assistant. Based on the patient's response: '{response}', generate {n} deep and specific follow-up questions to narrow down the problem.
    """
    general_q_template = """
    You are a medical AI assistant. Based on the patient's response: '{response}', generate {n} general questions to understand the patient's overall health condition.
    """

    deep_q_prompt = PromptTemplate(template=deep_q_template, input_variables=["response", "n"])
    general_q_prompt = PromptTemplate(template=general_q_template, input_variables=["response", "n"])

    deep_q_chain = LLMChain(prompt=deep_q_prompt, llm=llm)
    general_q_chain = LLMChain(prompt=general_q_prompt, llm=llm)

    deep_questions = deep_q_chain.run({"response": patient_response, "n": deep_questions})
    general_questions = general_q_chain.run({"response": patient_response, "n": general_questions})

    return deep_questions.split('\n'), general_questions.split('\n')

def generate_options(question):
    # For simplicity, generate dummy options
    options = [f"Option {i+1} for {question}" for i in range(4)]
    return options
