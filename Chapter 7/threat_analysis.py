import openai
import os
import json
import datetime

# ASCII Art Title
ascii_art = r"""

           /__  ___/ //    / / //   ) )  //   / /  // | |  /__  ___/         
             / /    //___ / / //___/ /  //____    //__| |    / /             
            / /    / ___   / / ___ (   / ____    / ___  |   / /              
           / /    //    / / //   | |  //        //    | |  / /               
          / /    //    / / //    | | //____/ / //     | | / /                
                                                          ___   ___          
    // | |     /|    / / // | |     / /  \\    / / //   ) )  / /    //   ) ) 
   //__| |    //|   / / //__| |    / /    \\  / / ((        / /    ((        
  / ___  |   // |  / / / ___  |   / /      \/ /    \\     / /       \\      
 //    | |  //  | / / //    | |  / /        / /       ) ) / /          ) )   
//     | | //   |/ / //     | | / /____/ / / / ((___ / /_/ /___ ((___ / /    

"""

print(ascii_art)

# Initialize the OpenAI API client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please configure your environment variables.")

def call_gpt(prompt):
    """
    Sends a prompt to OpenAI's API and retrieves the response.
    """
    messages = [
        {"role": "system", "content": "You are a cybersecurity SOC analyst with more than 25 years of experience."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Upgraded from gpt-3.5-turbo
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            api_key=OPENAI_API_KEY  # Ensure API key is passed correctly
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def save_report(content, file_name):
    """
    Saves the generated threat analysis to a .txt file in a dedicated folder.
    """
    folder_name = "threat_reports"
    os.makedirs(folder_name, exist_ok=True)  # Ensure the folder exists
    file_path = os.path.join(folder_name, file_name)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    print(f"\nThreat report saved to: {file_path}")

def analyze_threat_data(file_path):
    """
    Analyzes a threat data file (JSON or TXT) by identifying potential threats,
    extracting IoCs, and obtaining contextual threat intelligence.
    """
    try:
        # Detect file type based on extension
        if file_path.endswith(".json"):
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_data = json.load(file)  # Parse JSON
                raw_data_str = json.dumps(raw_data, indent=2)  # Convert JSON to string
        elif file_path.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_data_str = file.read().strip()
        else:
            print("Error: Unsupported file format. Use a .txt or .json file.")
            return
        
        if not raw_data_str:
            print("Error: The threat data file is empty.")
            return

        print("\nProcessing threat data...")

        # Query ChatGPT to identify and categorize potential threats
        identified_threats = call_gpt(f"Analyze the following threat data and identify potential threats:\n\n{raw_data_str}")
        
        # Extract IoCs (Indicators of Compromise)
        extracted_iocs = call_gpt(f"Extract all indicators of compromise (IoCs) from the following threat data:\n\n{raw_data_str}")
        
        # Obtain detailed context about the identified threats
        threat_context = call_gpt(f"Provide a detailed context or narrative behind the identified threats in this data:\n\n{raw_data_str}")

        # Print results
        print("\n=== Identified Threats ===\n")
        print(identified_threats or "No threats identified.")
        
        print("\n=== Extracted IoCs ===\n")
        print(extracted_iocs or "No IoCs found.")
        
        print("\n=== Threat Context ===\n")
        print(threat_context or "No additional context available.")

        # Save report to a file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file_name = f"threat_report_{timestamp}.txt"
        report_content = (
            f"=== Identified Threats ===\n{identified_threats or 'No threats identified.'}\n\n"
            f"=== Extracted IoCs ===\n{extracted_iocs or 'No IoCs found.'}\n\n"
            f"=== Threat Context ===\n{threat_context or 'No additional context available.'}\n"
        )
        save_report(report_content, report_file_name)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON file. Ensure the file contains valid JSON.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    file_path = input("Enter the path to the raw threat data (.txt or .json) file: ").strip()
    analyze_threat_data(file_path)
