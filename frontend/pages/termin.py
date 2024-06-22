import streamlit as st
import sqlite3

# Date, Location, Doctor name, Summary, Documents?

# Show Specific Termin:
# Have: TerID
# slotDate, locAddress, (docName, docSurname), summary, documents

# Upload Documents:
# Have: TerID
# INSERT INTO documents a blob


ex_termin = ("2024-06-25", "Max Mustermann", "Karlsruhe", None, "20489234", "abc@email.com")

termin_key = st.session_state.termin_key


def open_termin(termin):
    st.header("Termininformationen")
    st.write(termin_key)
    date = st.write("Date: " + termin[0])
    info = st.write(termin[1] + ", " + termin[2])
    summary = termin[3]
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
        st.button("Cancel Appointment")
    with c2:
        st.button("Reschedule Appointment")


# location = s
# docName
# patName
# sum


open_termin(ex_termin)
