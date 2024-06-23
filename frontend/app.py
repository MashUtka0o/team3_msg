import streamlit as st
from pages.doctor_module import doctor_homepage
from pages.patient_module import patient_homepage


# Define navigation function
def navigate_to(page):
    st.session_state.current_page = page


# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

# Landing page
if st.session_state.current_page == "landing":
    st.title("Welcome to the Medical Report Generator")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Doctor"):
            navigate_to("doctor_homepage")

    with col2:
        if st.button("Patient"):
            navigate_to("patient_homepage")

# Doctor homepage
elif st.session_state.current_page == "doctor_homepage":
    doctor_homepage()

# Patient homepage
elif st.session_state.current_page == "patient_homepage":
    patient_homepage()
