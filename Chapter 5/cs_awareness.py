import openai
import os
import threading
import time
from datetime import datetime
from tqdm import tqdm

# Set up the OpenAI API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
openai.api_key = api_key

# Generate a unique filename for the assessment
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
assessment_name = f"Cybersecurity_Assessment_{current_datetime}.txt"

def generate_question(categories: str) -> str:
    """
    Generate a cybersecurity awareness training assessment test.
    
    :param categories: Categories to base the assessment on.
    :return: Generated questions as a string.
    """
    messages = [
        {"role": "system", "content": "You are a cybersecurity professional and instructor with more than 25 years of experience."},
        {"role": "user", "content": f"Create a cybersecurity awareness training (for employees) assessment test. Provide no other response other than to create a question set of 10 cybersecurity awareness questions. Provide 4 multiple choice options with only one being the correct answer. After the question and answer choices, provide the correct answer and then provide a short contextual description. Provide no further generation or response.\n\nBase the assessment on the following categories:\n\n{categories}"},
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        temperature=0.7,
    )

    # Return the generated text
    return response.choices[0].message.content.strip()

def display_elapsed_time():
    """
    Display elapsed time in seconds while waiting for the API call to complete.
    """
    start_time = time.time()
    while not api_call_completed:
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

# Read content categories from the file
try:
    with open("trainingcontent.txt", "r") as file:
        content_categories = ', '.join([line.strip() for line in file.readlines()])
except FileNotFoundError:
    print("Error: 'trainingcontent.txt' file not found.")
    exit(1)

api_call_completed = False
elapsed_time_thread = threading.Thread(target=display_elapsed_time)
elapsed_time_thread.start()

# Generate the report using the OpenAI API
try:
    # Generate the question set
    questions = generate_question(content_categories)
    api_call_completed = True  # Mark API call as completed
except Exception as e:
    print(f"\nAn error occurred during the API call: {e}")
    api_call_completed = True  # Ensure thread termination
    exit(1)

elapsed_time_thread.join()  # Wait for the thread to finish

# Save the questions into a text file
try:
    with open(assessment_name, 'w') as file:
        file.write(questions)
    print(f"\nAssessment generated successfully and saved to {assessment_name}!")
except Exception as e:
    print(f"\nAn error occurred during the assessment generation: {e}")
