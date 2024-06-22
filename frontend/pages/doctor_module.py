import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from backend.summary_generator import MedicalReportGenerator
from backend.bio_sensor_data import get_dummy_bio_sensor_data
from backend import termin_manipulation

load_dotenv()
# Fetch configuration variables from environment variables

AOAI_ENDPOINT = os.environ.get("AOAI_ENDPOINT")
AOAI_KEY = os.environ.get("AOAI_KEY")
COMPLETIONS_DEPLOYMENT_NAME = "gpt-35-turbo"
AOAI_API_VERSION = "2023-09-01-preview"

st.title("Doctor Homepage")

doc_termin = termin_manipulation.get_doc_termin(1)
print(doc_termin)
# Sample list of patients for the day (This would be loaded from a database in a real application)
patients_of_the_day = [
    {"name": "Max Mustermann",
     "insurance_number": "XXXXX",
     "photo": "./frontend/backend/dummy_patients/max.png",
     "data_file": "./frontend/backend/dummy_patients/dummy_max.json",
     "appointment_time": "2024-06-25 08:30"},
    {"name": "John Doe",
     "insurance_number": "YYYYY",
     "photo": "./frontend/backend/dummy_patients/john.jpg",
     "data_file": "./frontend/backend/dummy_patients/dummy_john.json",
     "appointment_time": "2024-06-25 09:00"}
]

# Initialize session state to track selected patient
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None


def display_overview():
    st.subheader("Future Appointments")
    st.write("---")
    if doc_termin:
        for appointment in doc_termin:
            st.write(f"**Patients**: {appointment[1]} {appointment[2]}")
            st.write(f"**Date**: {appointment[3]}")
            st.write(f"**Time**: {appointment[4]}")
            if st.button(key=appointment[0], label="See More"):
                st.session_state.termin_key = appointment[0]
                st.switch_page("./pages/termin.py")
            st.write("---")
    else:
        st.write("No upcoming appointments")


def display_patient_list():
    st.subheader("Patients of the Day")
    for idx, patient in enumerate(patients_of_the_day):
        st.write(f"**{patient['name']}** - Insurance Number: {patient['insurance_number']}")
        if st.button(f"View {patient['name']}"):
            st.session_state.selected_patient = idx


def display_patient_details(patient):
    # Load patient data from the selected file
    with open(patient["data_file"], "r") as file:
        patient_data = json.load(file)

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
        st.write(" ")
        # st.header("Bio Sensor Data")
        # bio_sensor_data = get_dummy_bio_sensor_data()
        # st.subheader("Sport Activity Last Month")
        # st.line_chart(bio_sensor_data['sport_activity'])
        #
        # st.subheader("Heart Beat History Over Month")
        # st.line_chart(bio_sensor_data['heart_beat_history'])
        #
        # st.subheader("Sleep Data")
        # st.line_chart(bio_sensor_data['sleep_data'])

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


# Main application logic
if st.session_state.selected_patient is None:
    display_overview()
    display_patient_list()
else:
    display_patient_details(patients_of_the_day[st.session_state.selected_patient])
    if st.button("Back to Patient List"):
        st.session_state.selected_patient = None
