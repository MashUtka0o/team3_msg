import json
import streamlit as st
from backend import streamlitInStreamlit as form_maker

# Add Personal Information
#

question1 = {"type": 'text', "question": "Why are you ge?", "label": "ge"}
# Checklist
question2 = {"type": 'checklist',
             "question": "How are you feeling today?",
             "options": ["Good", "Bad", "I love beer"],
             "single": True,
             "label": "feeling"}
question2_other = {"type": 'checklist',
                   "question": "Choose?",
                   "options": ["Happy", "Sad", "No", "Why"],
                   "single": False,
                   "label": "choice"}

# Scale
question3 = {"type": 'scale',
             "question": "1-10?",
             "scale": [1, 5],
             "label": "1-10"}
ex_q_list = [question1, question2, question2_other, question3]

elif st.session_state.current_step == "deep_questions":
    st.header("Deep Questions")
    for i, question in enumerate(st.session_state.deep_questions):
        st.subheader(f"Question {i+1}: {question}")
        options = generate_options(question)
        answer = st.multiselect(f"Select answers for Question {i+1}", options)
        st.session_state.fragebogen["deep_questions"][question] = answer

out = form_maker.render_question_list(ex_q_list)

# location = st.radio("Wo sind ihre Schmerzen lokalisiert?",
#                     ["Innenseite", "Außenseite", "Weiß ich nicht"])
#
# time = st.radio("Wann haben die Schmerzen begonnen?", [
#     "1-3 Tagen", "4-7 Tagen", "bis 2 Wochen", "länger als 2 Wochen"])
#
# desc_of_pain = st.radio("Können Sie die Schmerzen beschreiben?", ["Stechen", "Brennen", "Weiß ich nicht"])
#
# if desc_of_pain == "Stechen":
#     desc_extra = st.radio("Haben Sie Symptome wie Taubheit, Schwäche?", ["Ja", "Nein"])
# else:
#     desc_extra = None
#
# event = st.text_area("Können Sie ein Ereignis beschreiben, nachdem die Schmerzen aufgetreten sind")

if st.button(label="Submit"):
    answers = out
    print(answers)
    output = {"Personal Information": {},
              "Answers": answers}
    print(output)

# Every form must have a submit button.
