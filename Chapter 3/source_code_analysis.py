import openai
import os
import ast
from ast import NodeVisitor
import threading
import time

# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

class CodeVisitor(NodeVisitor):
    def __init__(self):
        self.function_defs = []

    def visit_FunctionDef(self, node):
        self.function_defs.append(node.name)
        self.generic_visit(node)

def review_code(source_code: str) -> str:
    """
    Sends the source code to OpenAI API for security review.
    """
    messages = [
        {"role": "system", "content": "You are a seasoned security engineer with extensive experience in reviewing code for potential security vulnerabilities."},
        {"role": "user", "content": f"Please review the following Python code snippet. Identify any potential security flaws and then provide testing steps:\n\n{source_code}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def generate_test_script(testing_steps: str, output_file: str):
    """
    Saves the testing steps as a Python script file.
    """
    with open(output_file, 'w') as file:
        file.write(testing_steps)

def display_elapsed_time():
    """
    Displays the elapsed time while waiting for the API response.
    """
    start_time = time.time()
    while not api_call_completed:
        elapsed_time = time.time() - start_time
        print(f"\rCommunicating with the API - Elapsed time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)

# Main code execution
if __name__ == "__main__":
    # Load the source code
    try:
        with open('source_code.py', 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print("Error: The file 'source_code.py' was not found.")
        exit(1)

    # Parse the source code and extract function definitions
    visitor = CodeVisitor()
    visitor.visit(ast.parse(source_code))

    # Initialize threading for elapsed time display
    api_call_completed = False
    elapsed_time_thread = threading.Thread(target=display_elapsed_time)
    elapsed_time_thread.start()

    # Handle the API call
    try:
        testing_steps = review_code(source_code)
        api_call_completed = True
        elapsed_time_thread.join()
    except Exception as e:
        api_call_completed = True
        elapsed_time_thread.join()
        print(f"\nAn error occurred during the API call: {e}")
        exit(1)

    # Save the testing steps as a Python test script
    test_script_output_file = "test_script.py"
    try:
        generate_test_script(testing_steps, test_script_output_file)
        print("\nTest script generated successfully!")
    except Exception as e:
        print(f"\nAn error occurred during the test script generation: {e}")
