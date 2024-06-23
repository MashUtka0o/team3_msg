import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from backend.summary_generator import MedicalReportGenerator
from backend.bio_sensor_data import get_dummy_bio_sensor_data
from backend.termin_manipulation import get_doc_termin

load_dotenv()
# Fetch configuration variables from environment variables

AOAI_ENDPOINT = os.environ.get("AOAI_ENDPOINT")
AOAI_KEY = os.environ.get("AOAI_KEY")
COMPLETIONS_DEPLOYMENT_NAME = "gpt-35-turbo"
AOAI_API_VERSION = "2023-09-01-preview"

st.title("Doctor Homepage")
if 'doctor_appointments' not in st.session_state:
    st.session_state.doctor_appointments = get_doc_termin(1)

# Sample list of patients for the day (This would be loaded from a database in a real application)
patients_of_the_day = [
    {"name": "Max Mustermann",
     "insurance_number": "XXXXX",
     "photo": "./backend/dummy_patients/max.png",
     "data_file": "./backend/dummy_patients/dummy_max.json",
     "appointment_time": "2024-06-25 08:30"},
    {"name": "John Doe",
     "insurance_number": "YYYYY",
     "photo": "./backend/dummy_patients/john.jpg",
     "data_file": "./backend/dummy_patients/dummy_john.json",
     "appointment_time": "2024-06-25 09:00"}
]

print(os.getcwd())
fragenbogen_generated_path = "./fragebogen.json"
with open(fragenbogen_generated_path, "r") as file2:
    demo_patient_data = json.load(file2)

print(demo_patient_data)

map_info_dict = {
    "name": demo_patient_data["name"] + demo_patient_data["nachname"],
    "insurance_number": "ZZZZZZ",
    "photo": "./backend/dummy_patients/max.png",
    "data_file": None,
    "appointment_time": "2024-06-25 11:30"}

# append to the patients of the day list
patients_of_the_day.append(map_info_dict)

# Initialize session state to track selected patient
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None


def display_overview():
    st.subheader("Overview of the Day")
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("16:00", "%H:%M")
    slots = []

    while start_time <= end_time:
        slots.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=30)

    schedule = {slot: None for slot in slots}
    for patient in patients_of_the_day:
        appointment_time = datetime.strptime(patient["appointment_time"], "%Y-%m-%d %H:%M").strftime("%H:%M")
        schedule[appointment_time] = patient

    for slot, patient in schedule.items():
        if patient:
            if st.button(f"{slot} - {patient['name']}"):
                st.session_state.selected_patient = patients_of_the_day.index(patient)
        else:
            st.write(f"{slot} - Free")


def display_patient_list():
    st.subheader("Patients of the Day")
    for idx, patient in enumerate(patients_of_the_day):
        st.write(f"**{patient['name']}** - Insurance Number: {patient['insurance_number']}")
        if st.button(f"View {patient['name']}"):
            st.session_state.selected_patient = idx


def display_patient_list():
    st.subheader("Patients of the Day")
    for idx, patient in enumerate(patients_of_the_day):
        st.write(f"**{patient['name']}** - Insurance Number: {patient['insurance_number']}")
        if st.button(f"View {patient['name']}"):
            st.session_state.selected_patient = idx


def display_patient_details(patient):
    if patient["data_file"] is not None:
        # Load patient data from the selected file
        with open(patient["data_file"], "r") as file:
            patient_data = json.load(file)

    else:
        patient_data = {"personal_information": {
            "name": map_info_dict["name"],
            "birth_date": demo_patient_data["dob"],
            "gender": "Male",
            "address": "Musterstraße 12, 12345 Berlin",
            "phone": "01234-567890",
            "email": "test@example.com"},

            "medical_history": {
                "main_reason": demo_patient_data["purpose_of_visit"],
                "complaint_start_date": "1 week before",
                "complaint_onset": "Suddenly",
                "previous_similar_complaints": True,
                "previous_treatments": "None",
                "current_medications": "None"
            },
            "mobility_and_function": {
                "daily_activity_problems": None,
                "walking_distance": None,
                "mobility_aids": None
            }
            ,
            "pain_details": {
                "pain_scale": demo_patient_data["pain_scale"],
                "pain_location": demo_patient_data["pain_location"],
                "pain_timing": ["Morning", "During movement"],
                "pain_relief": "None",
                "pain_worsening": "None"
            },
            "additional_health_information": {
                "allergies": "None",
                "chronic_diseases": "None",
                "smoking": "None",
                "alcohol": "Yes, occasionally"
            },
            "additional_notes": demo_patient_data["followup_questions"]}

    # Display patient photo
    image = Image.open(patient["photo"])
    image = image.resize((200, 200))
    st.image(image, caption="Patient Photo", use_column_width=False)

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Summary",
        "Biometric data",
        "Scan and Documents",
        "Patient Information"
    ])

    with tab1:
        generator = MedicalReportGenerator(
            api_version=AOAI_API_VERSION,
            endpoint=AOAI_ENDPOINT,
            api_key=AOAI_KEY,
            deployment_name=COMPLETIONS_DEPLOYMENT_NAME
        )

        patient_data_flat = generator.flatten_patient_data(patient_data)
        report_content = generator.generate_report_content(patient_data_flat)

        st.header("Generated Medical Report Summary")
        st.text(report_content)

    with tab2:
        st.header("Bio Sensor Data")
        bio_sensor_data = get_dummy_bio_sensor_data()
        st.subheader("Sport Activity Last Month")
        st.line_chart(bio_sensor_data['sport_activity'])
        st.subheader("Heart Beat History Over Month")
        st.line_chart(bio_sensor_data['heart_beat_history'])

        st.subheader("Sleep Data")
        st.line_chart(bio_sensor_data['sleep_data'])

    with tab3:
        st.header("Scan and Documents")
        st.write("No documents available.")  # Placeholder for future documents

    with tab4:
        st.header(f"Patient Information for {patient_data['personal_information']['name']}")
        st.write(f"**Name**: {patient_data['personal_information']['name']}")
        st.write(f"**Insurance Number**: {patient['insurance_number']}")
        st.write(f"**Date of Birth**: {patient_data['personal_information']['birth_date']}")
        st.write(f"**Gender**: {patient_data['personal_information']['gender']}")
        st.write(f"**Address**: {patient_data['personal_information']['address']}")
        st.write(f"**Phone**: {patient_data['personal_information']['phone']}")
        st.write(f"**Email**: {patient_data['personal_information']['email']}")


def display_appointments(appointments):
    st.header("Your Appointments")
    if appointments:
        for appointment in appointments:
            st.write(f"**Patient**: {appointment[1]} {appointment[2]}")
            st.write(f"**Date**: {appointment[3]}")
            st.write(f"**Time**: {appointment[4]}")
            st.write(f"**Location**: {appointment[5]}")
            if st.button(key=appointment[0], label="See More"):
                st.session_state.termin_key = appointment[0]
                st.switch_page("./pages/doc_termin.py")
            st.write("---")
    else:
        st.write("No upcoming appointments")


# Main application logic
if st.session_state.selected_patient is None:
    display_overview()
    display_patient_list()

else:
    display_patient_details(patients_of_the_day[st.session_state.selected_patient])
    if st.button("Back to Patient List"):
        st.session_state.selected_patient = None

display_appointments(st.session_state.doctor_appointments)
