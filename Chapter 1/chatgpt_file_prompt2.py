import openai
import os

def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read().strip()  # Ensure no extra whitespace or newlines

def get_chat_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Load API key and prompt
openai.api_key = open_file('openai-key.txt')

# Load a single prompt from the file
prompt = open_file("prompt.txt")  # Prompt already stripped in open_file()

# Process the single prompt
print(f"Prompt: {prompt}")
response_text = get_chat_gpt_response(prompt)
print(f"Response: {response_text}")
