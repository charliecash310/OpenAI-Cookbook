import openai
import os
import subprocess
import time

# ASCII Art Title
ascii_art = """

              THE QUIETER YOU ARE

   / //_//   |  / /   /  _/  / ____/ __ \/_  __/
  / ,<  / /| | / /    / /   / / __/ /_/ / / /   
 / /| |/ ___ |/ /____/ /   / /_/ / ____/ / /    
/_/ |_/_/  |_/_____/___/   \____/_/     /_/     
              
             THE MORE ABLE TO HEAR

"""

print(ascii_art)

def open_file(filepath):
    """Open and read a file with error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        exit(1)

def save_file(filepath, content):
    """Create a new file or overwrite an existing one."""
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def append_file(filepath, content):
    """Append content to an existing file."""
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

# Load OpenAI API key from file
openai.api_key = open_file('openai-key.txt')

def gpt_3(prompt, retries=3, delay=5):
    """Sets up and runs the request to the OpenAI API with retries."""
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=600,
            )
            return response["choices"][0]["message"]["content"].strip()
        except openai.error.APIError as e:
            print(f"\nError communicating with the API. Attempt {attempt + 1} of {retries}")
            print(f"Error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                return "API Error: Unable to generate a response."

while True:
    request = input("\nEnter request (type 'quit' to exit): ")
    if not request or request.lower() == "quit":
        print("\nExiting program.")
        break

    # Load prompt template and replace placeholder with user input
    prompt_template = open_file("prompt4.txt").replace('{INPUT}', request)
    command = gpt_3(prompt_template)

    print("\nGenerated Command:\n", command)

    # Execute the command in the Linux shell
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if stdout:
        print(stdout)
    if stderr:
        print("\nError Output:\n", stderr)

    exit_code = process.wait()

    # Log the request and command execution details
    append_file("command-log.txt", f"Request: {request}\nCommand: {command}\nExit Code: {exit_code}\n\n")
