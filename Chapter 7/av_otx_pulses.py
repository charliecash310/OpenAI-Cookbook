import requests

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

# Send GET request
response = requests.get(OTX_URL, headers=headers)

# Check response status
if response.status_code == 200:
    # Save the data to a JSON file
    with open("otx_pulses.json", "w") as file:
        file.write(response.text)
    print("[+] Successfully retrieved AlienVault OTX Pulses!")
else:
    print(f"[-] Failed to retrieve data. HTTP Status: {response.status_code}")
    print(response.text)
