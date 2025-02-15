import requests
import datetime
import os

# ASCII Art Title
ascii_art = r"""

|\   __  \ |\  \      |\  \ |\  ___ \  |\   ___  \                                            
\ \  \|\  \\ \  \     \ \  \\ \   __/| \ \  \\ \  \                                           
 \ \   __  \\ \  \     \ \  \\ \  \_|/__\ \  \\ \  \                                          
  \ \  \ \  \\ \  \____ \ \  \\ \  \_|\ \\ \  \\ \  \                                         
   \ \__\ \__\\ \_______\\ \__\\ \_______\\ \__\\ \__\                                        
    \|__|\|__| \|_______| \|__|_\|_______|_\|__|_\|__|   ___    _________                     
                    |\  \    /  /||\   __  \ |\  \|\  \ |\  \  |\___   ___\                   
                    \ \  \  /  / /\ \  \|\  \\ \  \\\  \\ \  \ \|___ \  \_|                   
                     \ \  \/  / /  \ \   __  \\ \  \\\  \\ \  \     \ \  \                    
                      \ \    / /    \ \  \ \  \\ \  \\\  \\ \  \____ \ \  \                   
                       \ \__/ /      \ \__\ \__\\ \_______\\ \_______\\ \__\                  
     ________   ________\|__|/__    __\|__|\|__| \|_______| \|_______| \|__|                  
    |\   __  \ |\___   ___\ |\  \  /  /|                                                      
    \ \  \|\  \\|___ \  \_| \ \  \/  / /                                                      
     \ \  \\\  \    \ \  \   \ \    / /                                                       
      \ \  \\\  \    \ \  \   /     \/                                                        
       \ \_______\    \ \__\ /  /\   \                                                        
        \|_______|     \|__|/__/ /\ __\                                                       
                         ___|__|/ \|__|  ___   ___        ________   _______    ________      
                        |\   __  \ |\  \|\  \ |\  \      |\   ____\ |\  ___ \  |\   ____\     
                        \ \  \|\  \\ \  \\\  \\ \  \     \ \  \___|_\ \   __/| \ \  \___|_    
                         \ \   ____\\ \  \\\  \\ \  \     \ \_____  \\ \  \_|/__\ \_____  \   
                          \ \  \___| \ \  \\\  \\ \  \____ \|____|\  \\ \  \_|\ \\|____|\  \  
                           \ \__\     \ \_______\\ \_______\ ____\_\  \\ \_______\ ____\_\  \ 
                            \|__|      \|_______| \|_______||\_________\\|_______||\_________\
                                                            \|_________|          \|_________|       

"""

print(ascii_art)

# Define API Key and URL
OTX_API_KEY = "205db3e22e99246f6d9b1f7c7e7f3938d011ed4d534f6366672c341ba8a125cc"
OTX_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"

# Set headers
headers = {
    "X-OTX-API-KEY": OTX_API_KEY
}

# Generate a filename based on the current date and time
current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
json_filename = f"otx_pulses_{current_datetime}.json"
txt_filename = f"otx_pulses_{current_datetime}.txt"

# Create a folder for storing reports
report_folder = "otx_reports"
os.makedirs(report_folder, exist_ok=True)

# Full file paths
json_filepath = os.path.join(report_folder, json_filename)
txt_filepath = os.path.join(report_folder, txt_filename)

# Send GET request
response = requests.get(OTX_URL, headers=headers)

# Check response status
if response.status_code == 200:
    data = response.text
    
    # Save JSON data to a new file
    with open(json_filepath, "w", encoding="utf-8") as file:
        file.write(data)
    
    print(f"[+] Successfully retrieved AlienVault OTX Pulses and saved as {json_filepath}!")
    
    # Convert JSON response into human-readable format for the text file
    try:
        json_data = response.json()
        readable_data = "\n".join([f"- {pulse['name']}: {pulse.get('description', 'No description')}" for pulse in json_data.get('results', [])])
    except Exception as e:
        readable_data = f"Error parsing JSON data: {e}"
    
    # Save human-readable report to a text file
    with open(txt_filepath, "w", encoding="utf-8") as file:
        file.write(f"=== AlienVault OTX Pulses Report ({current_datetime}) ===\n\n{readable_data}\n")
    
    print(f"[+] Report also saved as {txt_filepath}!")
else:
    print(f"[-] Failed to retrieve data. HTTP Status: {response.status_code}")
    print(response.text)
