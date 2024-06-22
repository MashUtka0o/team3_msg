import json
import streamlit as st
from fragenbogen_generator import generate_questions, generate_options


st.title("Patient-Oriented Fragebogen")

if "fragebogen" not in st.session_state:
    st.session_state.fragebogen = {
        "initial_response": "",
        "deep_questions": {},
        "general_questions": {}
    }
    st.session_state.current_step = "initial_response"

if st.session_state.current_step == "initial_response":
    st.header("Initial Response")
    initial_response = st.text_input("Patient: What can I help you with today?")
    if st.button("Submit"):
        st.session_state.fragebogen["initial_response"] = initial_response
        st.session_state.deep_questions, st.session_state.general_questions = generate_questions(initial_response)
        st.session_state.current_step = "deep_questions"

elif st.session_state.current_step == "deep_questions":
    st.header("Deep Questions")
    for i, question in enumerate(st.session_state.deep_questions):
        st.subheader(f"Question {i+1}: {question}")
        options = generate_options(question)
        answer = st.multiselect(f"Select answers for Question {i+1}", options)
        st.session_state.fragebogen["deep_questions"][question] = answer

    if st.button("Next"):
        st.session_state.current_step = "general_questions"

elif st.session_state.current_step == "general_questions":
    st.header("General Questions")
    for i, question in enumerate(st.session_state.general_questions):
        st.subheader(f"Question {i+1}: {question}")
        options = generate_options(question)
        answer = st.multiselect(f"Select answers for Question {i+1}", options)
        st.session_state.fragebogen["general_questions"][question] = answer

    if st.button("Finish"):
        with open("fragebogen.json", "w") as f:
            json.dump(st.session_state.fragebogen, f, indent=4)
        st.success("Fragebogen saved successfully!")
        st.session_state.current_step = "completed"

elif st.session_state.current_step == "completed":
    st.header("Fragebogen Completed")
    st.write("Thank you for completing the questionnaire. The data has been saved.")
