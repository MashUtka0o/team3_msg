import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

chatClient = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_key=os.getenv("AOAI_KEY"),
    api_version="2023-05-15",
)

MODEL_NAME = "gpt-4"

followup_prompt = """
You are a helpful assistant that helps a doctor gather more details about a patient's acute pain.
 dont start your prompt with any intorduction , straight to the questions. 
 dont finish also with any closing sentences
 Here is an example output for patient visiting a  :
[
"Schildern Sie kurz Ihre aktuellen Beschwerden",
"Seit wann haben Sie diese Beschwerden?",
   - seit Stunden
   - Tagen
   - Wochen
   - Monaten
   - Jahren",
"Wie stark leiden Sie unter diesen Beschwerden?",
   - leicht
   - stark
   - sehr stark",
"Wurden Sie deswegen schon ärztlich behandelt?",
   - JA
   - NEIN",
"Wie sind diese Beschwerden bis jetzt behandelt worden?",
   - Medikamentös
   - Verödung
   - Gummibandligatur
   - Operation"
]

Given the pain details provided by the patient, generate 5 follow-up questions.
"""

# Given the pain details provided by the patient, generate 5 follow-up questions with max 4 suggestion with number e.g (1.XXXX) in order the patient put as answer.


def generate_followup_questions(pain_location, pain_type, pain_scale):
    chatResponse = chatClient.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{followup_prompt} \n The patient is experiencing {pain_type} pain located at {pain_location} with a pain scale of {pain_scale}/10."},
        ],
    )
    questions = chatResponse.choices[0].message.content.strip().split("\n")


    print(questions)

    return [question for question in questions[1:-2] if question]


