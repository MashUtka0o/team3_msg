import streamlit as st

patient_name = "John"
patient_surname = "Smith"
date = "12/04/2023"
time = "12:10"
important = ["questionnaire"]
contacts = ["maj.kak@gmail.com", "1232345615846"]
#important = []

st.title("Appointment Information")

def display_information(name, surname, date, time, important, contacts):
    st.markdown("""
        <style>
        .custom-expander{
            color: white;
            background-color: red;
            text-align: center;
        }
        .expander-title{
            color: white;
            background-color: red;
        }
        </style>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(f"<span style='font-size:18px; font-weight:bold;'>Patient Name: </span> {name}", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<span style='font-size:18px; font-weight:bold;'>Patient Surname: </span> {surname}", unsafe_allow_html=True)

    expanded = True if not important else False
    with st.expander('Important Information:', expanded=expanded):
        if important:
            for info in important:
                st.write(info)
        else:
            st.markdown(f'<div class="custom-expander">NO INFORMATION!</div>', unsafe_allow_html=True)

    with st.expander("Contact Information: "):
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.write(contacts[0])
        with c2:
            st.write(contacts[1])

    c1, c2 = st.columns(2)
    with c1:
        cancel_button = st.button("Cancel the Appointment")
    with c2:
        reschedule_button = st.button("Reschedule the Appointment")

display_information(patient_name, patient_surname, date, time, important, contacts)