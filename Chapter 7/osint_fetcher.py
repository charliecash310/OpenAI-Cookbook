import requests
import json

# ASCII Art Title
ascii_art = """
                                                                                                  
                    _____             ______   ____  _____   ______   _________________           
               ____|\    \        ___|\     \ |    ||\    \ |\     \ /                 \          
              /     /\    \      |    |\     \|    | \\    \| \     \\______     ______/          
             /     /  \    \     |    |/____/||    |  \|    \  \     |  \( /    /  )/             
            |     |    |    | ___|    \|   | ||    |   |     \  |    |   ' |   |   '              
            |     |    |    ||    \    \___|/ |    |   |      \ |    |     |   |                  
            |\     \  /    /||    |\     \    |    |   |    |\ \|    |    /   //                  
            | \_____\/____/ ||\ ___\|_____|   |____|   |____||\_____/|   /___//                   
             \ |    ||    | /| |    |     |   |    |   |    |/ \|   ||  |`   |                    
              \|____||____|/  \|____|_____|   |____|   |____|   |___|/  |____|                    
                 \(    )/        \(    )/       \(       \(       )/      \(                      
                  '    '          '    '         '        '       '        '                      
                                                                                                  
                                                                                                  
      _____       ______   _________________      _____    ____   ____      ______        _____   
 ____|\    \  ___|\     \ /                 \ ___|\    \  |    | |    | ___|\     \   ___|\    \  
|    | \    \|     \     \\______     ______//    /\    \ |    | |    ||     \     \ |    |\    \ 
|    |______/|     ,_____/|  \( /    /  )/  |    |  |    ||    |_|    ||     ,_____/||    | |    |
|    |----'\ |     \--'\_|/   ' |   |   '   |    |  |____||    .-.    ||     \--'\_|/|    |/____/ 
|    |_____/ |     /___/|       |   |       |    |   ____ |    | |    ||     /___/|  |    |\    \ 
|    |       |     \____|\     /   //       |    |  |    ||    | |    ||     \____|\ |    | |    |
|____|       |____ '     /|   /___//        |\ ___\/    /||____| |____||____ '     /||____| |____|
|    |       |    /_____/ |  |`   |         | |   /____/ ||    | |    ||    /_____/ ||    | |    |
|____|       |____|     | /  |____|          \|___|    | /|____| |____||____|     | /|____| |____|
  )/           \( |_____|/     \(              \( |____|/   \(     )/    \( |_____|/   \(     )/  
  '             '    )/         '               '   )/       '     '      '    )/       '     '   
                   _|/     \(              \( |____|/   \(     )/    \( |_____|/   \(     )/  
  '             '    )/         '               '   )/       '     '      '    )/       '     '   
                     '                              '                          '                  

"""

print(ascii_art)


# Replace with your AlienVault OTX API Key
OTX_API_KEY = "205db3e22e99246f6d9b1f7c7e7f3938d011ed4d534f6366672c341ba8a125cc"
OTX_BASE_URL = "https://otx.alienvault.com/api/v1"

# Function to get latest threat indicators
def get_otx_indicators():
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    url = f"{OTX_BASE_URL}/indicators/export"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open("otx_threat_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("[+] OTX Threat Data Saved.")
    else:
        print("[-] Failed to fetch OTX threat data.")

# Function to fetch recent CVEs
def get_latest_cves():
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0?recent=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open("nvd_cves.json", "w") as f:
            json.dump(data, f, indent=4)
        print("[+] Latest CVEs Saved.")
    else:
        print("[-] Failed to fetch CVEs.")

# Function to get Phishing URLs
def get_phishing_urls():
    url = "http://data.phishtank.com/data/online-valid.csv"
    response = requests.get(url)
    if response.status_code == 200:
        with open("phishing_urls.csv", "wb") as f:
            f.write(response.content)
        print("[+] Phishing URLs Saved.")
    else:
        print("[-] Failed to fetch phishing URLs.")

if __name__ == "__main__":
    print("[+] Fetching OSINT Threat Intelligence...")
    get_otx_indicators()
    get_latest_cves()
    get_phishing_urls()
    print("[+] OSINT Data Collection Complete.")
