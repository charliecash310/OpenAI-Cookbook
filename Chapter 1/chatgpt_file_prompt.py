import openai
import os

def open_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as infile:
        return infile.read()

def get_chat_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

openai.api_key = open_file('openai-key.txt')

# Load all prompts from the file
prompts = open_file("prompt.txt").strip().split('\n')  # Split by lines

# Process each prompt
for index, prompt in enumerate(prompts, start=1):
    print(f"Prompt {index}: {prompt}")
    response_text = get_chat_gpt_response(prompt)
    print(f"Response {index}: {response_text}\n")
