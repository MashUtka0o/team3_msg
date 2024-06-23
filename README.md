# Project: Patient-Doctor Communication Platform

## Overview
This project is designed to improve communication between patients and doctors. It provides a platform where patients can book appointments, fill out a detailed questionnaire (Fragenbogen), and keep track of their health records. Doctors can navigate between patients, view summaries of the questionnaires, and access biometric health data if needed. The tool is built using Streamlit, SQLite, and Azure OpenAI Chat to generate Fragenbogen questions and summarize the questionnaire, delivering concise information to the doctor.

## Features
1. **Fragenbogen During Appointment Booking**
   - Patients answer a dynamic questionnaire during the appointment booking process.
   - The Fragenbogen is generated according to the patient's answers, ensuring relevant follow-up questions.

2. **Booking and Canceling Appointments**
   - Patients can book and cancel appointments easily.
   - They can track their appointments and view their health records.

3. **Doctor's Platform**
   - Doctors can navigate between patients and see summaries of their questionnaires.
   - The platform provides a detailed overview of the patient's condition before the check-in.

4. **Biometric Health Data**
   - Doctors can check patients' biometric health data if needed.
   - This includes data such as heart rate, sleep patterns, and physical activity.

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: SQLite
- **AI Integration**: Azure OpenAI Chat

## Installation and Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/MashUtka0o/team3_msg.git
   cd team3_msg/frontend
   streamlit run index.py --theme.base "light" ```

