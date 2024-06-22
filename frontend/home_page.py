import streamlit as st

st.title("Welcome to XXXXXXXXXXXXX")
col1, col2 = st.columns(2)

with col1:
    if st.button("Doctor Profile"):
        st.switch_page("./pages/doctor_module.py")

with col2:
    if st.button("Patient Profile"):
        st.switch_page("./pages/patient_module.py")
