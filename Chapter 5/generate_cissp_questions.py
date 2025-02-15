import openai
import os
import threading
import time
from datetime import datetime

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Generate a timestamped filename
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
assessment_name = f"Exam_questions_{current_datetime}.txt"

# Function to generate CISSP questions
def generate_cissp_questions() -> str:
    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are a cybersecurity professional and training instructor with more than 25 years of experience."},
        {"role": "user", "content": "Help me study for the CISSP exam. Generate a list of 25 multiple choice questions, just as they will appear on the exam or practice exams. Present the question followed by the answer choices. After all of the questions have been listed, automatically provide an answer key without waiting for a prompt."},
    ]
    
    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        temperature=0.7,
    )
    # Return the generated content
    return response.choices[0].message["content"].strip()

# Function to display elapsed time while waiting for the API call
def display_elapsed_time():
    start_time = time.time()
    while not api_call_completed:
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

# Initialize a flag to track API call completion
api_call_completed = False

# Start the elapsed time thread
elapsed_time_thread = threading.Thread(target=display_elapsed_time)
elapsed_time_thread.start()

# Generate the questions using the OpenAI API
try:
    email_simulations = generate_cissp_questions()
    api_call_completed = True
except Exception as e:
    print(f"\nAn error occurred during the API call: {e}")
    api_call_completed = True
    elapsed_time_thread.join()
    exit()

# Wait for the elapsed time thread to finish
elapsed_time_thread.join()

# Save the generated questions to a text file
try:
    with open(assessment_name, 'w') as file:
        file.write(email_simulations)
    print("\nCISSP questions generated successfully!")
    print(f"Saved to file: {assessment_name}")
except Exception as e:
    print(f"\nAn error occurred while saving the file: {e}")