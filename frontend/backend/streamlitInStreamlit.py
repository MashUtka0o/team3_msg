import streamlit as st

# Example Question List

if 'components_list' not in st.session_state:
    st.session_state.components_list = []


# Question Type: text, multiple_checklist, single_checklist, discrete_scale
# Text


def render_question(question):
    out = None
    q_type = question["type"]
    q_text = question["question"]
    q_label = question["label"]
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
                out.append([st.checkbox(option), option])
    elif q_type == "scale":
        scale = question["scale"]
        out = st.slider(q_text, scale[0], scale[1])
    else:
        print("Question Type Not Found")
    return q_label, out


def render_question_list(question_list):
    answer_list = []
    for question in question_list:
        answer_list.append(render_question(question))
    answer_dict = {key: value for key, value in answer_list}
    return answer_dict


def add_question():
    q_text = st.text_input("Question")
    type_selected = st.selectbox("Question Type", ["Checklist", "Scale", "Text"])
    if type_selected == "Checklist":
        q_type = "checklist"
        st.button("Add Option")
        st.checkbox("Allow Multiple Choices?")
    elif type_selected == "Scale":
        q_type = "scale"
        min = st.text_input("Minimum Value")
        max = st.text_input("Maximum Value")
    elif type_selected == "Text":
        q_type = 'text'
    return


def render_questions_list(question_list):
    return


def save_list():
    return

# Form Component Looks like this:
