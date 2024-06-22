import streamlit as st
from datetime import datetime
from backend import termin_manipulation
from backend.termin_manipulation import termin_creation, attach_file_to_termin
import time
import random
import os

# Notifications:
# Have: patID
# Get: ter

# Appointments:
# Have: patID
# Get: terID, (docName, docSurname), slotDate, slotTime, locAddress

data = termin_manipulation.get_one_patient(1)[0]

patient_data = {"name": data[0],
                "nachname": data[1],
                "dob": data[2]}
print(patient_data)

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
        {"doctor": "Dr. Smith", "date": "2024-06-25", "time": "10:00 AM", "id": 1, "summary": " "},
        {"doctor": "Dr. Wolfl", "date": "2024-06-26", "time": "2:00 PM", "id": 2, "summary": "Broken leg"}
    ]

prescriptions = [
    {"doctor": "Dr. Schasn", "medication": "Paracetamol", "date": "2024-06-20",
     "instruction": "Twice per day after food."},
    {"doctor": "Dr. Smith", "medication": "Ibuprofen", "date": "2024-06-19",
     "instruction": "Once per day. Can be taken before or after food."}
]

slots_taken = [1, 2, 45, 23]
user_id = 1


def generate_uid():
    random_int = random.randint(1, 1000000)
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    id = (timestamp << 20) | random_int  # Shift timestamp and combine with random int
    return id


def display_notifications(notifications):
    with st.expander("Notifications: ", expanded=True):  # st.sidebar.header
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
        for appointment in appointment_list:
            st.write(f"**Doctor**: {appointment[1]} {appointment[2]}")
            st.write(f"**Date**: {appointment[3]}")
            st.write(f"**Time**: {appointment[4]}")
            if st.button(key=appointment[0], label="See More"):
                st.session_state.termin_key = appointment[0]
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
    global appointment_list
    st.header("Book a New Appointment")
    appointment_id = generate_uid()
    location = st.multiselect("Location:", location_list)
    doctor_type = st.multiselect("Doctor type:", doc_type_list)
    doc_list = termin_manipulation.get_doc(doctor_type)
    if doc_list:
        doctor = st.selectbox("Doctor:", doc_list)
        slot_list = termin_manipulation.get_free_slots(location, doctor)
        if slot_list:
            slots = st.selectbox("Slots Available", slot_list)
            date = st.date_input("Select Date")
            time = st.time_input("Select Time")
        else:
            st.write("No Slots Available")
        files = st.file_uploader("Select files", type="pdf", accept_multiple_files=True)
        if 'files' not in st.session_state:
            st.session_state.files = []
        if 'path' not in st.session_state:
            st.session_state.path = None
        st.session_state.file_names = []
        if files:
            st.session_state.files.extend(files)
            for file in st.session_state.files:
                if not os.path.exists("tempDir"):
                    os.makedirs("tempDir")
                with open(os.path.join("tempDir", file.name), "wb") as f:
                    f.write(file.getbuffer())
                st.session_state.path = os.path.abspath(os.path.join('tempDir', file.name))
        if st.button("Book Appointment"):
            if 'file_names' not in st.session_state:
                st.session_state.file_names = []
            st.session_state.file_names = []
            for file in st.session_state.files:
                attach_file_to_termin(appointment_id, st.session_state.path)
                st.session_state.file_names.append(file.name)
            st.session_state.files = []
            new_appointment = {
                "location": location,
                "doctor type": doctor_type,
                "doctor": doctor,
                "date": date.strftime("%Y-%m-%d"),
                "time": time.strftime("%I:%M %p"),
                "summary": " ",
                "files": st.session_state.file_names,
                "id": appointment_id
            }
            st.session_state.file_names = []
            slot_id = generate_uid()
            slots_taken.append(slot_id)
            st.session_state.appointments.append(new_appointment)
            st.success("Appointment booked successfully!")
            termin_creation(slot_id, 1)  # slot_id and pat_id
            appointment_list = termin_manipulation.get_pat_termin(1)
        st.session_state.files = []
        st.session_state.file_names = []
        st.session_state.path = None
    else:
        st.write("No Doctor Found")


tab1, tab2 = st.tabs(["Appointments", "Prescriptions"])

with tab1:
    book_appointment()
    display_appointments(appointment_list)

with tab2:
    display_prescriptions(prescriptions)

back = st.button("Back to Home Page")
if back:
    st.switch_page("./home_page.py")


def display_menu():
    st.sidebar.title("Menu")
    st.sidebar.write("---")
    st.sidebar.button("Smart Stats")
    st.sidebar.write("---")
    st.sidebar.button("Connections")
    st.sidebar.write("---")
    st.sidebar.button("Health Plan")
    st.sidebar.write("---")
    st.sidebar.button("Documents")
    st.sidebar.write("---")
    st.sidebar.button("Settings")


display_menu()
