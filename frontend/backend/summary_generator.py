import json
from fpdf import FPDF
from langchain import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage


class MedicalReportGenerator:
    def __init__(self, api_version, endpoint, api_key, deployment_name):
        self.api_version = api_version
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.llm = AzureChatOpenAI(
            temperature=0,
            openai_api_version=self.api_version,
            azure_endpoint=self.endpoint,
            openai_api_key=self.api_key,
            azure_deployment=self.deployment_name
        )

    def load_json(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def flatten_patient_data(self, patient_data):
        """ flatten the answers from the fragenbogen"""
        patient_data_flat = {
            **patient_data['personal_information'],
            **patient_data['medical_history'],
            **patient_data['pain_details'],
            **patient_data['mobility_and_function'],
            **patient_data['additional_health_information'],
            **{'additional_notes': patient_data['additional_notes']}
        }
        patient_data_flat['pain_location'] = ", ".join(patient_data_flat['pain_location'])
        patient_data_flat['pain_timing'] = ", ".join(patient_data_flat['pain_timing'])
        return patient_data_flat

    def generate_report_content(self, patient_data_flat):
        """ define a prompt that integrate inforamtion from the fragenbogen for the LLM model 
        and invoke the content """

        custom_prompt_template = """
            Generate a detailed medical summary for the doctor based on the following patient data.
            Dont recommend anything to the doctor; you are an assistant to the doctor, just summarizing the information about the patient.
            only return a summary from the given informations. 

            Patient Information:
            - Name: {name}
            - Date of Birth: {birth_date}
            - Gender: {gender}
            - Address: {address}
            - Phone: {phone}
            - Email: {email}

            Medical History:
            - Main Reason for Visit: {main_reason}
            - Complaint Start Date: {complaint_start_date}
            - Complaint Onset: {complaint_onset}
            - Previous Similar Complaints: {previous_similar_complaints}
            - Previous Treatments: {previous_treatments}
            - Current Medications: {current_medications}

            Pain Details:
            - Pain Scale: {pain_scale}/10
            - Pain Location: {pain_location}
            - Pain Timing: {pain_timing}
            - Pain Relief: {pain_relief}
            - Pain Worsening Factors: {pain_worsening}

            Mobility and Function:
            - Problems with Daily Activities: {daily_activity_problems}
            - Walking Distance Without Pain: {walking_distance}
            - Use of Mobility Aids: {mobility_aids}

            Additional Health Information:
            - Allergies: {allergies}
            - Chronic Diseases: {chronic_diseases}
            - Smoking: {smoking}
            - Alcohol Consumption: {alcohol}

            Additional Notes:
            - {additional_notes}
            Only Return a Summary in PARAGRAPH form, format it with new lines
        """

        custom_prompt = PromptTemplate(template=custom_prompt_template, input_variables=list(patient_data_flat.keys()))
        message_content = custom_prompt.format(**patient_data_flat)
        messages = [HumanMessage(content=message_content)]
        response = self.llm(messages=messages)

        return response.content
