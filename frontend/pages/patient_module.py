import streamlit as st
from datetime import datetime

# Sample data for notifications, appointments, and prescriptions
notifications = [
    "Your appointment with Dr. Smith is confirmed for tomorrow.",
    "You have a new prescription from Dr. Brown."
]

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
    st.sidebar.header("Notifications")
    if notifications:
        for note in notifications:
            st.sidebar.write(f"- {note}")
    else:
        st.sidebar.write("No new notifications")


def display_appointments(appointments):
    st.header("Your Appointments")
    if appointments:
        for appointment in appointments:
            st.write(f"**Doctor**: {appointment['doctor']}")
            st.write(f"**Date**: {appointment['date']}")
            st.write(f"**Time**: {appointment['time']}")
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
    location = st.multiselect("Location:", ["All", "Karlsruhe", "Deggendorf", "Berlin"], default="All")
    doctor_type = st.multiselect("Doctor type:", ["All", "General Practice", "Surgeon", "Psychotherapist"],
                                 default="All")
    doctor = st.multiselect("Doctor:", ["All", "Marina Schultz", "John Smith"], default="All")
    date = st.date_input("Select Date")
    time = st.time_input("Select Time")
    if st.button("Book Appointment"):
        new_appointment = {
            "location": location,
            "doctor type": doctor_type,
            "doctor": doctor,
            "date": date.strftime("%Y-%m-%d"),
            "time": time.strftime("%I:%M %p")
        }
        st.session_state.appointments.append(new_appointment)
        st.success("Appointment booked successfully!")
        st.experimental_rerun()


display_notifications(notifications)

tab1, tab2 = st.tabs(["Appointments", "Prescriptions"])

with tab1:
    display_appointments(st.session_state.appointments)
    book_appointment()

with tab2:
    display_prescriptions(prescriptions)
