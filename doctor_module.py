import os
import json
import streamlit as st
from summary_generator import MedicalReportGenerator
from dotenv import load_dotenv

_ = load_dotenv()
# Fetch configuration variables from environment variables

AOAI_ENDPOINT = os.environ.get("AOAI_ENDPOINT")
AOAI_KEY = os.environ.get("AOAI_KEY")
COMPLETIONS_DEPLOYMENT_NAME = "gpt-35-turbo"
AOAI_API_VERSION = "2023-09-01-preview"

def doctor_homepage():
    st.title("Doctor Homepage")

    # Automatically load the dummy JSON file (TODO database)
    json_file_path = "team3_msg/dummy_max.json"
    with open(json_file_path, "r") as file:
        patient_data = json.load(file)

    # Display patient photo (TODO database)
    st.image("team3_msg/max.png",
             caption="Patient Photo",
             use_column_width=True)

    # Display patient information
    st.header(f"Patient Information for {patient_data['personal_information']['name']}")
    st.write(f"**Name**: {patient_data['personal_information']['name']}")
    st.write(f"**Insurance Number**: XXXXX")
    st.write(f"**Date of Birth**: {patient_data['personal_information']['birth_date']}")
    st.write(f"**Gender**: {patient_data['personal_information']['gender']}")
    st.write(f"**Address**: {patient_data['personal_information']['address']}")
    st.write(f"**Phone**: {patient_data['personal_information']['phone']}")
    st.write(f"**Email**: {patient_data['personal_information']['email']}")


    generator = MedicalReportGenerator(
        api_version=AOAI_API_VERSION,
        endpoint=AOAI_ENDPOINT,
        api_key=AOAI_KEY,
        deployment_name=COMPLETIONS_DEPLOYMENT_NAME
    )

    patient_data_flat = generator.flatten_patient_data(patient_data)
    report_content = generator.generate_report_content(patient_data_flat)

    st.subheader("Generated Medical Report Summary from the Fragenbogen")
    st.text(report_content)
