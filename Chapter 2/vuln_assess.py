import openai
import os
import threading
import time
from datetime import datetime
from tqdm import tqdm

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
assessment_name = f"Vuln_Assessment_Plan_{current_datetime}"

def read_user_input_file(file_path: str) -> dict:
    user_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':', 1)
            user_data[key.strip()] = value.strip()
    return user_data

user_data_file = "assessment_data.txt"
user_data = read_user_input_file(user_data_file)

def generate_report(network_size, number_of_nodes, type_of_devices, special_devices, operating_systems,
                    network_topology, access_controls, previous_security_incidents, compliance_requirements,
                    business_critical_assets, data_classification, goals, timeline, team, deliverables, audience: str) -> str:
    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are a cybersecurity professional specializing in vulnerability assessment."},
        {"role": "user", "content": f'''Using cybersecurity industry standards and best practices, create a complete and detailed
        vulnerability assessment plan (not a penetration test). Include the following sections:
        1. Introduction: Provide context and purpose.
        2. Process/Methodology: Detailed outline of the approach, including policies, procedures, compliance, and technical methods.
        3. Tools Required: List tools for scanning, configuration review, etc.
        4. Assessment Steps: Comprehensive step-by-step plan.

        Tailor the plan using these details:
        Network Size: {network_size}
        Number of Nodes: {number_of_nodes}
        Type of Devices: {type_of_devices}
        Excluded Devices: {special_devices}
        Operating Systems: {operating_systems}
        Network Topology: {network_topology}
        Access Controls: {access_controls}
        Previous Security Incidents: {previous_security_incidents}
        Compliance Requirements: {compliance_requirements}
        Business Critical Assets: {business_critical_assets}
        Data Classification: {data_classification}
        Goals: {goals}
        Timeline: {timeline}
        Team: {team}
        Deliverables: {deliverables}
        Audience: {audience}'''}
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=3000,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']

def save_to_file(text: str, file_path: str):
    with open(file_path, 'w') as file:
        file.write(text)

def display_elapsed_time():
    start_time = time.time()
    while not api_call_completed:
        elapsed_time = time.time() - start_time
        print(f"\rCommunicating with the API - Elapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

api_call_completed = False
elapsed_time_thread = threading.Thread(target=display_elapsed_time)
elapsed_time_thread.start()

try:
    # Generate the report using the OpenAI API
    report = generate_report(
        user_data["Network Size"],
        user_data["Number of Nodes"],
        user_data["Type of Devices"],
        user_data["Specific systems or devices that need to be excluded from the assessment"],
        user_data["Operating Systems"],
        user_data["Network Topology"],
        user_data["Access Controls"],
        user_data["Previous Security Incidents"],
        user_data["Compliance Requirements"],
        user_data["Business Critical Assets"],
        user_data["Data Classification"],
        user_data["Goals and objectives of the vulnerability assessment"],
        user_data["Timeline for the vulnerability assessment"],
        user_data["Team"],
        user_data["Expected deliverables of the assessment"],
        user_data["Audience"]
    )
    api_call_completed = True
    elapsed_time_thread.join()

    # Save the report to a Markdown file
    markdown_output_file = f"{assessment_name}_report.md"
    with tqdm(total=1, desc="Generating plan") as pbar:
        save_to_file(report, markdown_output_file)
        pbar.update(1)

    print("\nPlan generated successfully!")
    print(f"Saved as: {markdown_output_file}")
except Exception as e:
    api_call_completed = True
    elapsed_time_thread.join()
    print(f"\nAn error occurred during the API call: {e}")
