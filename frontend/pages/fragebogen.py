import json
import streamlit as st
from backend.fragenbogen_generator import generate_followup_questions
from backend import termin_manipulation

st.title("Patient-Oriented Fragebogen")


def reset_fragebogen():
    st.session_state.fragebogen = {
        "purpose_of_visit": "",
        "pain_location": "",
        "pain_type": "",
        "pain_scale": 0,
        "followup_questions": {},
        "control_answers": {}
    }
    st.session_state.current_step = "initial_response"
    st.session_state.followup_questions = []
    st.session_state.qa_overview = []


if "fragebogen" not in st.session_state:
    reset_fragebogen()

if st.button("Reset Fragebogen"):
    reset_fragebogen()
    st.experimental_rerun()

if st.session_state.current_step == "initial_response":
    st.header("What can I help you with today?")
    purpose_of_visit = st.selectbox("What is the purpose of your visit today?", ["Acute pain", "Control"])
    st.session_state.fragebogen["purpose_of_visit"] = purpose_of_visit
    if purpose_of_visit == "Control":
        st.session_state.control_questions = [
            "How have you been since your last treatment?",
            "Any new symptoms or concerns?",
            "Are you taking your medications as prescribed?",
            "When was your last visit?",
            "Any side effects from the treatment?"
        ]
        st.session_state.current_step = "control_questions"
    else:
        st.session_state.current_step = "pain_details"

elif st.session_state.current_step == "pain_details":
    st.header("Pain Details")
    pain_location = st.text_input("Where is the pain located?")
    pain_type = st.selectbox("What type of pain are you experiencing?",
                             ["Sharp", "Dull", "Throbbing", "Burning", "Other"])
    pain_scale = st.slider("On a scale of 1 to 10, how would you rate your pain?", 1, 10)

    if st.button("Submit Pain Details"):
        st.session_state.fragebogen["pain_location"] = pain_location
        st.session_state.fragebogen["pain_type"] = pain_type
        st.session_state.fragebogen["pain_scale"] = pain_scale
        st.session_state.qa_overview.append(("Pain Location", pain_location))
        st.session_state.qa_overview.append(("Pain Type", pain_type))
        st.session_state.qa_overview.append(("Pain Scale", pain_scale))

        # Generate follow-up questions using LLM
        followup_questions = generate_followup_questions(pain_location, pain_type, pain_scale)
        st.session_state.followup_questions = followup_questions
        st.session_state.current_step = "followup_questions"

elif st.session_state.current_step == "followup_questions":
    st.header("Follow-up Questions")
    for i, question in enumerate(st.session_state.followup_questions):
        st.subheader(f"Question {i + 1}: {question}")
        answer = st.text_area(f"Answer for Question {i + 1}", key=f"followup_{i}")
        st.session_state.fragebogen["followup_questions"][question] = answer
        st.session_state.qa_overview.append((question, answer))

    if st.button("Finish and Save"):
        data = termin_manipulation.get_one_patient(1)[0]
        patient_data = {"name": data[0],
                        "nachname": data[1],
                        "dob": data[2]}
        json_dump = {**st.session_state.fragebogen, **patient_data}
        # with open("fragebogen.json", "w") as f:
        #     json.dump(json_dump, f, indent=4)
        # st.session_state.summary_result = Call A function
        st.success("Fragebogen saved successfully!")
        st.session_state.current_step = "completed"

elif st.session_state.current_step == "control_questions":
    st.header("Control Visit Questions")
    for i, question in enumerate(st.session_state.control_questions):
        st.subheader(f"Question {i + 1}: {question}")
        answer = st.text_area(f"Answer for Question {i + 1}", key=f"control_{i}")
        st.session_state.fragebogen["control_answers"][question] = answer
        st.session_state.qa_overview.append((question, answer))

    if st.button("Finish and Save"):
        data = termin_manipulation.get_one_patient(1)[0]
        patient_data = {"name": data[0],
                        "nachname": data[1],
                        "dob": data[2]}

        json_dump = {**st.session_state.fragebogen, **patient_data}

        with open("fragebogen.json", "w") as f:
            json.dump(json_dump, f, indent=4)

        st.success("Fragebogen saved successfully!")
        st.session_state.current_step = "completed"

elif st.session_state.current_step == "completed":
    st.header("Fragebogen Completed")
    st.write("Thank you for completing the questionnaire. The data has been saved.")

# Display the Q/A overview section
if st.session_state.qa_overview:
    st.header("Q/A Overview")
    for q, a in st.session_state.qa_overview:
        st.write(f"**Q: {q}**")
        if isinstance(a, list):
            st.write(f"**A:** {', '.join(a)}")
        else:
            st.write(f"**A:** {a}")
