import openai
import os
import threading
import time
from datetime import datetime

# Set up the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Generate a timestamped assessment filename
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
assessment_name = f"Email_Simulations_{current_datetime}.txt"

# Function to generate email simulations
def generate_email_simulations() -> str:
    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are a cybersecurity professional and expert in adversarial social engineering tactics, techniques, and procedures, with 25 years of experience."},
        {"role": "user", "content": "Create a list of fictitious emails for an interactive email phishing training. The emails can represent a legitimate email or a phishing attempt, using one or more various techniques. After each email, provide the answer, contextual descriptions, and details for any other relevant information such as the URL for any links in the email, header information. Generate all necessary information in the email and supporting details. Present 3 simulations in total. At least one of the simulations should simulate a real email."},
    ]

    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        raise RuntimeError(f"API call failed: {e}")

# Function to display elapsed time while waiting for the API call
def display_elapsed_time():
    start_time = time.time()
    while not api_call_completed:
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

# Flag to track API call completion
api_call_completed = False

# Start a thread to display elapsed time
elapsed_time_thread = threading.Thread(target=display_elapsed_time)
elapsed_time_thread.start()

# Generate the report using the OpenAI API
try:
    # Generate the email simulations
    email_simulations = generate_email_simulations()
except Exception as e:
    print(f"\nAn error occurred during the API call: {e}")
    api_call_completed = True
    elapsed_time_thread.join()
    exit(1)

# Mark API call as completed and wait for the thread to finish
api_call_completed = True
elapsed_time_thread.join()

# Save the email simulations into a text file
try:
    with open(assessment_name, 'w') as file:
        file.write(email_simulations)
    print(f"\nEmail simulations generated successfully and saved to {assessment_name}!")
except Exception as e:
    print(f"\nAn error occurred while saving the email simulations: {e}")
    exit(1)
