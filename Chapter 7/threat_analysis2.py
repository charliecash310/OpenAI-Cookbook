import openai
import os
import json
import re

# ASCII Art Title
ascii_art = r"""
       _____ __  ______  _____________  _________ 
      / ___// / / / __ \/  _/ ____/   |/_  __/   |
      \__ \/ / / / /_/ // // /   / /| | / / / /| |
     ___/ / /_/ / _, _// // /___/ ___ |/ / / ___ |
    /____/\____/_/ |_/___/\____/_/__|_/_/_/_/  |_|
        /_  __/ / / / __ \/ ____/   |/_  __/      
         / / / /_/ / /_/ / __/ / /| | / /         
        / / / __  / _, _/ /___/ ___ |/ /          
    ___/_/ /_/ /_/_/ |_/_____/_/__|_/_/________   
   /   |  / | / /   |  / /\ \/ / ___//  _/ ___/   
  / /| | /  |/ / /| | / /  \  /\__ \ / / \__ \    
 / ___ |/ /|  / ___ |/ /___/ /___/ // / ___/ /    
/_/  |_/_/ |_/_/  |_/_____/_//____/___//____/     
                                                  
"""

print(ascii_art)

# Initialize the OpenAI API client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY  # Correctly set API key

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please configure your environment variables.")

def call_gpt(prompt):
    """
    Sends a prompt to OpenAI's API and retrieves the response.
    """
    messages = [
        {"role": "system", "content": "You are a cybersecurity SOC analyst with more than 25 years of experience."},
        {"role": "user", "content": prompt[:4000]}  # Limit input size
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def parse_fast_log(file_path):
    """
    Parses Suricata fast.log and extracts relevant details for analysis.
    """
    logs = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r"(\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}.\d{6})\s+\[\*\*\]\s+(.+?)\s+\[\*\*\]\s+\[Classification:\s(.+?)\]\s+\[Priority:\s(\d+)\]\s+\{\s*(\w+)\s*\}\s+(\d+\.\d+\.\d+\.\d+):(\d+)\s*->\s*(\d+\.\d+\.\d+\.\d+):(\d+)", line)
                
                if match:
                    logs.append({
                        "timestamp": match.group(1),
                        "alert": match.group(2),
                        "classification": match.group(3),
                        "priority": match.group(4),
                        "protocol": match.group(5),
                        "src_ip": match.group(6),
                        "src_port": match.group(7),
                        "dest_ip": match.group(8),
                        "dest_port": match.group(9),
                    })

        return logs

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def analyze_threat_data(file_path):
    """
    Processes fast.log and sends extracted threat data to GPT.
    """
    logs = parse_fast_log(file_path)

    if not logs:
        print("No valid log entries found.")
        return

    formatted_logs = json.dumps(logs[:20], indent=2)  # Send first 20 logs to GPT to prevent overload
    
    print("\nProcessing threat data...")

    # Query ChatGPT to identify and categorize potential threats
    identified_threats = call_gpt(f"Analyze the following Suricata fast.log data and identify potential threats:\n\n{formatted_logs}")
    
    # Extract IoCs (Indicators of Compromise)
    extracted_iocs = call_gpt(f"Extract all indicators of compromise (IoCs) from the following threat data:\n\n{formatted_logs}")
    
    # Obtain detailed context about the identified threats
    threat_context = call_gpt(f"Provide a detailed context or narrative behind the identified threats in this data:\n\n{formatted_logs}")

    # Print results
    print("\n=== Identified Threats ===\n", identified_threats or "No threats identified.")
    print("\n=== Extracted IoCs ===\n", extracted_iocs or "No IoCs found.")
    print("\n=== Threat Context ===\n", threat_context or "No additional context available.")

if __name__ == "__main__":
    file_path = input("Enter the path to the Suricata fast.log file: ").strip()
    analyze_threat_data(file_path)
