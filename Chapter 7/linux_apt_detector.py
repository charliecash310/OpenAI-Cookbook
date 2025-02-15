import subprocess
import os
import openai

# ASCII Art Title
ascii_art = """
    ___    ____  ______                            
   /   |  / __ \/_  __/                            
  / /| | / /_/ / / /                               
 / ___ |/ ____/ / /                                
/_/ _|_/_/_____/_/__________________________  ____ 
   / __ \/ ____/_  __/ ____/ ____/_  __/ __ \/ __ \
  / / / / __/   / / / __/ / /     / / / / / / /_/ /
 / /_/ / /___  / / / /___/ /___  / / / /_/ / _, _/ 
/_____/_____/ /_/ /_____/\____/ /_/  \____/_/ |_|                                           

"""

print(ascii_art)

# Initialize OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it before running the script.")

openai.api_key = openai_api_key

# Function to interact with OpenAI GPT
def call_gpt(prompt):
    try:
        messages = [
            {"role": "system", "content": "You are a cybersecurity SOC analyst with extensive experience in Linux threat detection."},
            {"role": "user", "content": prompt[:5000]}  # Truncate input to avoid exceeding token limits
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=512,  # Reduce response size to fit within limits
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

# Function to run a shell command safely
def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return result.stdout.strip()[:5000]  # Truncate long output
    except Exception as e:
        return f"Error running command: {e}"

# Commands for Linux APT detection
commands = {
    "Process Data": "ps aux --sort=-%cpu | head -20",  # Show top CPU-consuming processes
    "Network Data": "netstat -tunapl | head -20",  # Active network connections with process info
    "Running Services": "systemctl list-units --type=service --state=running | head -20",  # Running services
    "Scheduled Tasks": "crontab -l 2>/dev/null || echo 'No crontab for current user'",  # Cron jobs
    "Security Logs": "journalctl -n 10 --no-pager",  # Last 10 security logs
    "Failed Login Attempts": "lastb | head -10",  # Last 10 failed login attempts
}

# Gather system data
system_data = {}
for key, cmd in commands.items():
    system_data[key] = run_command(cmd)

# Format data for GPT analysis
analysis_prompt = "Analyze the following Linux system data for signs of Advanced Persistent Threats (APTs):\n\n"
for key, data in system_data.items():
    analysis_prompt += f"{key}:\n{data}\n\n"

# Analyze with GPT
analysis_result = call_gpt(analysis_prompt)

# Display results
print("\n=== Linux System Analysis ===")
for key, data in system_data.items():
    print(f"\n[{key}]\n{data}\n")

print("\n=== AI Security Analysis ===")
print(analysis_result)
