import requests
import json
import time
from bs4 import BeautifulSoup

# ASCII Art Title
ascii_art = """
     _             _             _           _                   _          _            _      
       / /\         /\ \           /\ \        / /\                /\ \       /\ \         /\ \    
      / /  \       /  \ \         /  \ \      / /  \              /  \ \     /  \ \       /  \ \   
     / / /\ \__   / /\ \ \       / /\ \ \    / / /\ \            / /\ \ \   / /\ \ \     / /\ \ \  
    / / /\ \___\ / / /\ \ \     / / /\ \_\  / / /\ \ \          / / /\ \_\ / / /\ \_\   / / /\ \_\ 
    \ \ \ \/___// / /  \ \_\   / / /_/ / / / / /  \ \ \        / / /_/ / // /_/_ \/_/  / / /_/ / / 
     \ \ \     / / /    \/_/  / / /__\/ / / / /___/ /\ \      / / /__\/ // /____/\    / / /__\/ /  
 _    \ \ \   / / /          / / /_____/ / / /_____/ /\ \    / / /_____// /\____\/   / / /_____/   
/_/\__/ / /  / / /________  / / /\ \ \  / /_________/\ \ \  / / /      / / /______  / / /\ \ \     
\ \/___/ /  / / /_________\/ / /  \ \ \/ / /_       __\ \_\/ / /      / / /_______\/ / /  \ \ \    
 \_____\/   \/____________/\/_/    \_\/\_\___\     /____/_/\/_/       \/__________/\/_/    \_\/    
                                                                                                  
"""

print(ascii_art)


# Define sources
SOURCES = {
    "KrebsOnSecurity": "https://krebsonsecurity.com/",
    "BleepingComputer": "https://www.bleepingcomputer.com/",
    "HackerNews": "https://thehackernews.com/",
    "CISA": "https://www.cisa.gov/news-events/alerts",
    "US-CERT": "https://www.us-cert.gov/ncas/alerts"
}

# Function to scrape text content from a webpage
def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = '\n'.join([p.get_text() for p in paragraphs if p.get_text()])
        return text_content[:1000]  # Limit to first 1000 characters for readability
    except requests.exceptions.RequestException as e:
        return f"Error retrieving data from {url}: {e}"

# Fetch and store data
def collect_threat_data():
    with open("threat_data.txt", "w", encoding="utf-8") as file:
        for source, url in SOURCES.items():
            print(f"Scraping {source}...")
            data = scrape_website(url)
            file.write(f"\n=== {source} ({url}) ===\n")
            file.write(data + "\n")
            time.sleep(2)  # Avoid rapid requests
    print("Threat data collection complete. Data saved in 'threat_data.txt'.")

if __name__ == "__main__":
    collect_threat_data()