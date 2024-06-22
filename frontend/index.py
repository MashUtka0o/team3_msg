import streamlit as st

if 'termin_key' not in st.session_state:
    st.session_state.termin_key = None

pg = st.navigation([st.Page("./home_page.py"), st.Page("./pages/termin.py"), st.Page("./pages/fragebogen.py"),
                    st.Page("./pages/patient_module.py"), st.Page("./pages/doctor_module.py")],
                   position='hidden')

pg.run()
