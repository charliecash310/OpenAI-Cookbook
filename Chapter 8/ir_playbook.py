import openai
import os
import datetime

# ASCII Art Title
ascii_art = r"""
 _____ __   _ _______ _____ ______  _______ __   _ _______     
   |   | \  | |         |   |     \ |______ | \  |    |        
 __|__ |  \_| |_____  __|__ |_____/ |______ |  \_|    |        
                                                               
  ______ _______ _______  _____   _____  __   _ _______ _______
 |_____/ |______ |______ |_____] |     | | \  | |______ |______
 |    \_ |______ ______| |       |_____| |  \_| ______| |______
                                                               
  _____         _______ __   __ ______   _____   _____  _     _
 |_____] |      |_____|   \_/   |_____] |     | |     | |____/ 
 |       |_____ |     |    |    |_____] |_____| |_____| |    \_
                                                                                                                                                      
"""

print(ascii_art)



def generate_incident_response_playbook(threat_type, environment_details):
    """
    Generate an incident response playbook based on the
    provided threat type and environment details.
    """
    # Create the messages for the OpenAI API
    messages = [
        {"role": "system", "content": "You are an AI assistant helping to create an incident response playbook."},
        {"role": "user", "content": f"Create a detailed incident response playbook for handling a '{threat_type}' threat affecting the following environment: {environment_details}."}
    ]

    # Make the API call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Get input from the user
    threat_type = input("Enter the threat type: ")
    environment_details = input("Enter environment details: ")
    
    # Generate the playbook
    playbook = generate_incident_response_playbook(threat_type, environment_details)
    
    # Print the generated playbook
    if playbook:
        print("\nGenerated Incident Response Playbook:")
        print(playbook)
        
        # Save to a uniquely named plaintext file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"incident_response_playbook_{timestamp}.txt"
        
        with open(filename, "w") as file:
            file.write(playbook)
            print(f"\nPlaybook saved as '{filename}'")
    else:
        print("Failed to generate the playbook.")

