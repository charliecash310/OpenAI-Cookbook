import openai
import os

# Load the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chat_gpt_response(prompt):
    # Generate a chat completion using GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.7
    )
    # Return the content of the response
    return response.choices[0].message.content.strip()

# Prompt for the AI
prompt = "Who is part of President Trump's cabinet?."
response_text = get_chat_gpt_response(prompt)
print(response_text)
