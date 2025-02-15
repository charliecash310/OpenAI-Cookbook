import openai
import os
import time
import threading
from tqdm import tqdm
from datetime import datetime

# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to generate a report using the OpenAI API
def generate_report(threat_name: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a professional cyber threat analyst and MITRE ATT&CK Framework expert."
        },
        {
            "role": "user",
            "content": f'''Provide a detailed report about {threat_name}, using the following template 
(and proper markdown language formatting, headings, bold keywords, tables, etc.):
            
# Threat Name
{threat_name}

## Summary
Short executive summary.

## Details
Description and details including:
- History/Background
- Discovery
- Characteristics and TTPs
- Known incidents

## MITRE ATT&CK TTPs
Table containing all known MITRE ATT&CK TTPs used by {threat_name}. Columns:
- **Tactic**
- **Technique ID**
- **Technique Name**
- **Procedure (How {threat_name} uses it)**

## Indicators of Compromise
Table containing all known indicators of compromise. Columns:
- **Type**
- **Value**
- **Description**
            '''
        }
    ]

    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Failed to generate the report: {e}")


# Function to save the report as a Markdown file
def save_as_markdown(text: str, output_file: str):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Report saved successfully as: {output_file}")
    except Exception as e:
        raise Exception(f"Failed to save the report: {e}")


# Function to display elapsed time while waiting for the API call
def display_elapsed_time():
    start_time = time.time()
    while not api_call_completed:
        elapsed_time = time.time() - start_time
        print(f"\rCommunicating with the API - Elapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)


# Main program
if __name__ == "__main__":
    # Get user input for the threat name
    threat_name = input("Enter the name of a cyber threat: ")

    # Set up threading for progress display
    api_call_completed = False
    elapsed_time_thread = threading.Thread(target=display_elapsed_time)
    elapsed_time_thread.start()

    try:
        # Generate the report
        report = generate_report(threat_name)
        api_call_completed = True
        elapsed_time_thread.join()

        # Save the report to a Markdown file
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = f"{threat_name}_report_{current_datetime}.md"
        with tqdm(total=1, desc="Saving report") as pbar:
            save_as_markdown(report, output_file)
            pbar.update(1)

    except Exception as e:
        api_call_completed = True
        elapsed_time_thread.join()
        print(f"\nAn error occurred: {e}")
