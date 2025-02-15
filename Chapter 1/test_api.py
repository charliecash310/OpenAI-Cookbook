import os
import openai

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Make sure to set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

# Example usage: Generate a response using GPT-4
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain the importance of cybersecurity in today's world."}
        ],
        max_tokens=150
    )
    print("Response:")
    print(response['choices'][0]['message']['content'].strip())
except Exception as e:
    print(f"An error occurred: {e}")
