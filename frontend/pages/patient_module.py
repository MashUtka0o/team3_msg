import streamlit as st
import time
from frontend.backend.termin_manipulation import termin_creation, attach_file_to_termin
import random
import os

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
user_id = 3452

def generate_uid():
    random_int = random.randint(1, 1000000)
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    id = (timestamp << 20) | random_int  # Shift timestamp and combine with random int
    return id
def display_notifications(notifications):
    with st.expander("Notifications: ", expanded=True): #st.sidebar.header
        if notifications:
            for idx, note in enumerate(notifications):
                checked = st.checkbox(f"{note}" if not st.session_state.checked_notifications[idx] else f"~~{note}~~", key=f"notification_{idx}", value=st.session_state.checked_notifications[idx])
                if checked != st.session_state.checked_notifications[idx]:
                    st.session_state.checked_notifications[idx] = checked
                    st.experimental_rerun()
        else:
            st.write("No new notifications")

def update_notifications():
    st.session_state.notifications = [note for idx, note in enumerate(st.session_state.notifications) if not st.session_state.checked_notifications[idx]]
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
                st.session_state.termin_key = appointment['id']
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


def book_appointment(slots_taken, user_id):
    st.header("Book a New Appointment")
    appointment_id = generate_uid()
    location = st.selectbox("Location:", ["All", "Karlsruhe", "Deggendorf", "Berlin"], index=0)
    doctor_type = st.selectbox("Doctor type:", ["All", "General Practice", "Surgeon", "Psychotherapist"],
                                 index=0)
    doctor = st.selectbox("Doctor:", ["All", "Marina Schultz", "John Smith"], index=0)
    date = st.date_input("Select Date")
    time = st.time_input("Select Time")
    files = st.file_uploader("Select files", type="pdf", accept_multiple_files=True)
    if 'files' not in st.session_state:
        st.session_state.files = []
    st.session_state.file_names = []
    if files:
        st.session_state.files.extend(files)
        for file in st.session_state.files:
            if not os.path.exists("tempDir"):
                os.makedirs("tempDir")
            with open(os.path.join("tempDir", file.name), "wb") as f:
                f.write(file.getbuffer())
            path = os.path.abspath(os.path.join('tempDir', file.name))
            attach_file_to_termin(appointment_id, path)



    if st.button("Book Appointment"):
        if 'file_names' not in st.session_state:
            st.session_state.file_names = []
        st.session_state.file_names = []
        for file in st.session_state.files:
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
        termin_creation(slot_id, user_id) #slot_id and pat_id
    st.session_state.files = []

tab1, tab2 = st.tabs(["Appointments", "Prescriptions"])

with tab1:
    book_appointment(slots_taken, user_id)
    display_appointments(st.session_state.appointments)

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