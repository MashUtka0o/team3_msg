import streamlit as st

st.header("Code&Create Group 3")

if 'notifications' not in st.session_state:
    st.session_state.notifications = ["Your appointment with Dr. Smith is confirmed for tomorrow.",
                     "You have a new prescription from Dr. Brown."]  # sample data, later change to data from db

if 'checked_notifications' not in st.session_state:
    st.session_state.checked_notifications = [False] * len(st.session_state.notifications)

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
    c1, c2 = st.columns(2)
    with c1:
        location = st.multiselect("Location: ",
                                  ("All", "Karlsruhe", "Deggendorf", "Berkin"), placeholder="Search For Location"),
    with c2:
        doctor_type = st.multiselect("Doctor type: ",
                                     ("All", "General Practice", "Surgeon", "Psychotherapist"),
                                     placeholder="Search for Doctor")
    doctor = st.multiselect("Doctor: ",
                            ("All", "Marina Schultz", "John Smith"))
    date = st.date_input("Select Date")
    time = st.time_input("Select Time")
    if st.button("Book Appointment"):
        new_appointment = {"location": location, "doctor type": doctor_type, "doctor": doctor,
                           "date": date.strftime("%Y-%m-%d"), "time": time.strftime("%I:%M %p")}
        st.session_state.appointments.append(new_appointment)
        st.success("Appointment booked successfully!")
        st.experimental_rerun()


tab1, tab2 = st.tabs(["Appointments", "Prescriptions"])

with tab1:
    book_appointment()
    display_appointments(st.session_state.appointments)

with tab2:
    display_prescriptions(prescriptions)

