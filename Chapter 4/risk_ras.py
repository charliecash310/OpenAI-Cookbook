import openai
import os
import threading
import time
from datetime import datetime
from tqdm import tqdm

# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Generate current datetime for unique assessment name
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
assessment_name = f"Risk_Assessment_Plan_{current_datetime}"

# Cyber Risk Assessment Report Outline
risk_assessment_outline = [
    "Executive Summary",
    "Introduction",
    "Asset Discovery/Identification",
    "System Characterization/Classification",
    "Network Diagrams and Data Flow Review",
    "Risk Pre-Screening",
    "Security Policy & Procedures Review",
    "Cybersecurity Standards Selection and Gap Assessment/Audit",
    "Vulnerability Assessment",
    "Threat Assessment",
    "Attack Vector Assessment",
    "Risk Scenario Creation (using the Mitre ATT&CK Framework)",
    "Validate Findings with Penetration Testing/Red Teaming",
    "Risk Analysis (Aggregate Findings & Calculate Risk Scores)",
    "Prioritize Risks",
    "Assign Mitigation Methods and Tasks",
    "Conclusion and Recommendations",
    "Appendix",
]

# Function to generate a section content using the OpenAI API
def generate_section_content(section: str, system_data: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a cybersecurity professional specializing in governance, risk, and compliance (GRC) with more than 25 years of experience."
        },
        {
            "role": "user",
            "content": f"You are currently writing a cyber risk assessment report. Write the context/details for the following section (and only this section): {section}. Use the provided system data for context. If no specific data is provided, include placeholder content aligned with industry standards.\n\n{system_data}"
        },
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating content for section '{section}': {e}")

# Read system data from a file
def load_system_data(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The system data file '{file_path}' does not exist.")

# Display elapsed time while waiting for the API call
def display_elapsed_time(api_call_completed_event):
    start_time = time.time()
    while not api_call_completed_event.is_set():
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

# Main script
if __name__ == "__main__":
    system_data_file = "systemdata.txt"
    system_data = load_system_data(system_data_file)

    api_call_completed_event = threading.Event()
    elapsed_time_thread = threading.Thread(target=display_elapsed_time, args=(api_call_completed_event,))
    elapsed_time_thread.start()

    report = []
    try:
        with tqdm(total=len(risk_assessment_outline), desc="Generating sections") as pbar:
            for section in risk_assessment_outline:
                content = generate_section_content(section, system_data)
                report.append(f"## {section}\n{content}")
                pbar.update(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        api_call_completed_event.set()
        elapsed_time_thread.join()

    # Save the report as a markdown file
    markdown_output_file = f"{assessment_name}_report.md"
    try:
        with open(markdown_output_file, 'w') as md_file:
            md_file.write('\n'.join(report))
        print(f"\nReport generated successfully: {markdown_output_file}")
    except Exception as e:
        print(f"\nAn error occurred while saving the report: {e}")
