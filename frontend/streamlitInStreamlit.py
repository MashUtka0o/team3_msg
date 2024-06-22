import streamlit as st

# Example Question List


# Question Type: text, multiple_checklist, single_checklist, discrete_scale
# Text
question1 = {"type": 'text', "question": "Why are you ge?"}
# Checklist
question2 = {"type": 'checklist',
             "question": "How are you feeling today?",
             "options": ["Good", "Bad", "I love beer"],
             "single": True}
question2_other = {"type": 'checklist',
                   "question": "Choose?",
                   "options": ["Happy", "Sad", "No", "Why"],
                   "single": False}

# Scale
question3 = {"type": 'scale',
             "question": "1-10?",
             "scale": [1, 5]}

ex_q_list = [question1, question2, question2_other, question3]

curr_question_list = []


def render_question(question):
    out = None
    q_type = question["type"]
    q_text = question["question"]
    if q_type == 'text':
        out = st.text_area(q_text)
    elif q_type == "checklist":
        single = question["single"]
        if single:
            out = st.radio(q_text, question["options"])
        else:
            out = []
            st.write(q_text)
            for option in question["options"]:
                out.append(st.checkbox(option))
    elif q_type == "scale":
        scale = question["scale"]
        out = st.slider(q_text, scale[0], scale[1])
    else:
        print("Question Type Not Found")
    return out


def render_question_list(question_list):
    answer_list = []
    for question in question_list:
        answer_list.append(render_question(question))
    return answer_list


test = render_question_list(ex_q_list)


def add_question():
    q_text = st.text_input("Question")
    q_type = st.selectbox("Question Type", ["Checklist", "Scale", ""])
    return


def render_questions_list(question_list):
    return


def save_list():
    return


def printsmt():
    st.write(test)


st.button("Add Question", on_click=add_question)
st.button("Save List", on_click=save_list)
st.button("show_answers", on_click=printsmt)

# Form Component Looks like this:
