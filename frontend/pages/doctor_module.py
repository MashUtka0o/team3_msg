import os
import json
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from backend.summary_generator import MedicalReportGenerator
from backend.bio_sensor_data import get_dummy_bio_sensor_data



load_dotenv()
# Fetch configuration variables from environment variables

AOAI_ENDPOINT = os.environ.get("AOAI_ENDPOINT")
AOAI_KEY = os.environ.get("AOAI_KEY")
COMPLETIONS_DEPLOYMENT_NAME = "gpt-35-turbo"
AOAI_API_VERSION = "2023-09-01-preview"


st.title("Doctor Homepage")

# Automatically load the dummy JSON file (TODO database)
json_file_path = "team3_msg/frontend/backend/dummy_max.json"
with open(json_file_path, "r") as file:
    patient_data = json.load(file)

# Display patient photo (TODO database)
image = Image.open("team3_msg/frontend/backend/max.png")
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
    st.write(f"**Insurance Number**: XXXXX")
    st.write(f"**Date of Birth**: {patient_data['personal_information']['birth_date']}")
    st.write(f"**Gender**: {patient_data['personal_information']['gender']}")
    st.write(f"**Address**: {patient_data['personal_information']['address']}")
    st.write(f"**Phone**: {patient_data['personal_information']['phone']}")
    st.write(f"**Email**: {patient_data['personal_information']['email']}")
