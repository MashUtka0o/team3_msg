import streamlit as st
import sqlite3
from backend.termin_manipulation import termin_cancelation, get_one_termin, get_pat_termin

# Date, Location, Doctor name, Summary, Documents?
termin_key = st.session_state.termin_key
# print(f"termin key: {termin_key}")
# # termin_info = [appointment for appointment in st.session_state.appointments if appointment['id'] == termin_key]
# # termin_info = termin_info[0]


termin_db_info = get_one_termin(termin_key)

print(termin_db_info)


# def open_termin(termin):
#     st.header("Appointment Information")
#     print(f"Termin info: {termin}")
#     st.write(termin_key)
#     date = st.write(f"Date: {termin['date']}")
#     time = st.write(f"Time:  {termin['time']}")
#     doctor = st.write(f"Doctor:  {termin['doctor']}")
#     st.write("Files: ")
#     for file in termin['files']:
#         st.write(file)
#     summary = None
#     if summary is None:
#         st.write(":red[Form not Filled, Please Fill Form]")
#     # This Button Opens a small tab
#
#     with st.expander("Important Information"):
#         st.write("Please bring with you all of your money in your bank account")
#         if summary is None:
#             if st.button("Fill in Form NOW"):
#                 st.switch_page("./pages/fragebogen.py")
#
#     c1, c2, c3 = st.columns([1, 1, 2])
#     with c1:
#         if st.button("Cancel Appointment"):
#             termin_cancelation(termin_key)
#             st.session_state.appointments = [appointment for appointment in st.session_state.appointments if
#                                              appointment['id'] != termin['id']]
#             st.switch_page("./pages/patient_module.py")
#     with c2:
#         st.button("Reschedule Appointment")
#
#     back = st.button("Back")
#     if back:
#         st.switch_page("./pages/patient_module.py")


def open_termin(termin):
    st.header("Appointment Information")
    st.write(termin_key)
    date = st.write(f"Date: {termin[0]}")
    time = st.write(f"Time:  {termin[1]}")
    doctor = st.write(f"Doctor: {termin[2]} {termin[3]}")
    address = st.write(f"Address: {termin[4]}")
    st.write("Files: ")
    # for file in termin['files']:
    #     st.write(file)
    summary = termin[5]
    if summary is None:
        st.write(":red[Form not Filled, Please Fill Form]")
    # This Button Opens a small tab
    with st.expander("Important Information"):
        st.write("Please bring with you all of your money in your bank account")
        if summary is None:
            if st.button("Fill in Form NOW"):
                st.switch_page("./pages/fragebogen.py")

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("Cancel Appointment"):
            termin_cancelation(termin_key)
            # st.session_state.appointments = get_pat_termin(1)
            st.switch_page("./pages/patient_module.py")
        st.session_state.appointments = get_pat_termin(1)
    with c2:
        st.button("Reschedule Appointment")

    back = st.button("Back")
    if back:
        st.switch_page("./pages/patient_module.py")


# location = s
# docName
# patName
# sum


open_termin(termin_db_info)
