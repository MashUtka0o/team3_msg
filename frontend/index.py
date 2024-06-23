import streamlit as st

if 'termin_key' not in st.session_state:
    st.session_state.termin_key = None
st.set_page_config(
    initial_sidebar_state="collapsed"
)

if st.sidebar.button("Switch to patient"):
    st.switch_page("./pages/patient_module.py")
if st.sidebar.button("Switch to doctor"):
    st.switch_page("./pages/doctor_module.py")
if st.sidebar.button("Home"):
    st.switch_page("./home_page.py")

pg = st.navigation([st.Page("./home_page.py"), st.Page("./pages/termin.py"), st.Page("./pages/fragebogen.py"),
                    st.Page("./pages/patient_module.py"), st.Page("./pages/doctor_module.py"),
                    st.Page("./pages/doc_termin.py")],
                   position='hidden')

pg.run()
