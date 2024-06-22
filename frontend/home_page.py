import streamlit as st

st.title("Welcome to the Medical Report Generator")
col1, col2 = st.columns(2)

with col1:
    if st.button("Doctor"):
        st.switch_page("./pages/doctor_module.py")

with col2:
    if st.button("Patient"):
        st.switch_page("./pages/patient_module.py")
