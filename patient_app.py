import streamlit as st
from datetime import datetime

notifications = ["Your appointment with Dr. Smith is confirmed for tomorrow.",
                 "You have a new prescription from Dr. Brown."] # sample data, later change to data from db

if 'appointments' not in st.session_state:
    st.session_state.appointments = [
        {"doctor": "Dr. Smith", "date": "2024-06-25", "time": "10:00 AM"},
        {"doctor": "Dr. Wolfl", "date": "2024-06-26", "time": "2:00 PM"}
    ]

prescriptions = [
    {"doctor": "Dr. Schasn", "medication": "Paracetamol", "date": "2024-06-20", "instruction": "Twice per day. After "
                                                                                               "the food."},
    {"doctor": "Dr. Smith", "medication": "Ibuprofen", "date": "2024-06-19", "instruction": "Once per day. Can be "
                                                                                            "taken before or after "
                                                                                            "the food."}
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
        for date in appointments:
            st.write(f"**Doctor**: {date['doctor']}")
            st.write(f"**Date**: {date['date']}")
            st.write(f"**Time**: {date['time']}")
            st.write("---")
    else:
        st.write("No upcoming appointments")

def display_prescriptions(prescriptions):
    st.header("Your Preinscriptions")
    if prescriptions:
        for note in prescriptions:
            st.write(f"**Medication**: {note['medication']}")
            st.write(f"**Date**: {note['date']}")
            st.write(f"**Instruction**: {note['instruction']}")
            st.write("---")
    else:
        st.write("You don't have any prescriptions")
def book_appointment():
    st.header("Book a New Appointment")
    location = st.multiselect("Location: ",
    ("All", "Karlsruhe", "Deggendorf", "Berkin"),
               default="All")
    doctor_type = st.multiselect("Doctor type: ",
                   ("All", "General Practice", "Surgeon", "Psychotherapist"),
                   default="All")
    doctor = st.multiselect("Doctor: ",
                   ("All", "Marina Schultz", "John Smith"),
                   default="All")
    date = st.date_input("Select Date")
    time = st.time_input("Select Time")
    if st.button("Book Appointment"):
        new_appointment = {"location": location, "doctor type": doctor_type, "doctor": doctor, "date": date.strftime("%Y-%m-%d"), "time": time.strftime("%I:%M %p")}
        st.session_state.appointments.append(new_appointment)
        st.success("Appointment booked successfully!")
        st.experimental_rerun()

tab1, tab2 = st.tabs(["Appointments", "Prescriptions"])

with tab1:
    display_appointments(st.session_state.appointments)
    book_appointment()

with tab2:
    display_prescriptions(prescriptions)


display_notifications(notifications)