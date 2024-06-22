import streamlit as st
from datetime import datetime
from backend import termin_manipulation

# Notifications:
# Have: patID
# Get: ter

# Appointments:
# Have: patID
# Get: terID, (docName, docSurname), slotDate, slotTime, locAddress


appointment_list = termin_manipulation.get_pat_termin(1)
location_list = termin_manipulation.get_loc()
doc_type_list = termin_manipulation.get_doctor_type()

# Sample data for notifications, appointments, and prescriptions
if 'notifications' not in st.session_state:
    st.session_state.notifications = ["Your appointment with Dr. Smith is confirmed for tomorrow.",
                                      "You have a new prescription from Dr. Brown."]

if 'checked_notifications' not in st.session_state:
    st.session_state.checked_notifications = [False] * len(st.session_state.notifications)

if 'appointments' not in st.session_state:
    st.session_state.appointments = [
        {"doctor": "Dr. Smith", "date": "2024-06-25", "time": "10:00 AM"},
        {"doctor": "Dr. Wolfl", "date": "2024-06-26", "time": "2:00 PM"}
    ]

prescriptions = [
    {"doctor": "Dr. Schasn", "medication": "Paracetamol", "date": "2024-06-20",
     "instruction": "Twice per day after food."},
    {"doctor": "Dr. Smith", "medication": "Ibuprofen", "date": "2024-06-19",
     "instruction": "Once per day. Can be taken before or after food."}
]


def display_notifications(notifications):
    with st.expander("Notifications: ", expanded=True): #st.sidebar.header
        if notifications:
            for idx, note in enumerate(notifications):
                checked = st.checkbox(f"{note}" if not st.session_state.checked_notifications[idx] else f"~~{note}~~",
                                      key=f"notification_{idx}", value=st.session_state.checked_notifications[idx])
                if checked != st.session_state.checked_notifications[idx]:
                    st.session_state.checked_notifications[idx] = checked
                    st.experimental_rerun()
        else:
            st.write("No new notifications")


def update_notifications():
    st.session_state.notifications = [note for idx, note in enumerate(st.session_state.notifications) if
                                      not st.session_state.checked_notifications[idx]]
    st.session_state.checked_notifications = [False] * len(st.session_state.notifications)


display_notifications(st.session_state.notifications)

if st.button("Update notifications"):
    update_notifications()
    st.experimental_rerun()


def display_appointments(appointments):
    st.header("Your Appointments")
    if appointments:
        for appointment in appointments:
            st.write(f"**Doctor**: {appointment['doctor']}")
            st.write(f"**Date**: {appointment['date']}")
            st.write(f"**Time**: {appointment['time']}")
            if st.button(key=appointment, label="See More"):
                st.session_state.termin_key = 12345
                st.switch_page("./pages/termin.py")
            st.write("---")


    else:
        st.write("No upcoming appointments")


def display_prescriptions(prescriptions):
    st.header("Your Prescriptions")
    if prescriptions:
        for prescription in prescriptions:
            st.write(f"**Medication**: {prescription['medication']}")
            st.write(f"**Date**: {prescription['date']}")
            st.write(f"**Instruction**: {prescription['instruction']}")
            st.write("---")
    else:
        st.write("You don't have any prescriptions")


def book_appointment():
    st.header("Book a New Appointment")
    location = st.multiselect("Location:", location_list)
    doctor_type = st.multiselect("Doctor type:", doc_type_list)
    doc_list = termin_manipulation.get_doc(doctor_type)
    if doc_list:
        doctor = st.selectbox("Doctor:", doc_list)
        slot_list = termin_manipulation.get_free_slots(location, doctor)

        if slot_list:
            slots = st.selectbox("Slots Available", slot_list)
        else:
            st.write("No Slots Available")
        if st.button("Book Appointment"):
            st.write("Fkjdshlfdskj")
    else:
        st.write("No Doctor Found")

tab1, tab2 = st.tabs(["Appointments", "Prescriptions"])

with tab1:
    book_appointment()
    display_appointments(st.session_state.appointments)

with tab2:
    display_prescriptions(prescriptions)

back = st.button("Back to Home Page")
if back:
    st.switch_page("./home_page.py")

def display_menu():
    st.sidebar.title("Menu")
    st.sidebar.write("---")
    st.sidebar.write("Smart Stats")
    st.sidebar.write("---")
    st.sidebar.write("Connections")
    st.sidebar.write("---")
    st.sidebar.write("Health Plan")
    st.sidebar.write("---")
    st.sidebar.write("Documents")
    st.sidebar.write("---")
    st.sidebar.write("Settings")


display_menu()
