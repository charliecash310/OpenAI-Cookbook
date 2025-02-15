import requests
import time

# ASCII Art Title
ascii_art = """

|\   ____\|\   __  \|\   __  \|\   ____\|\  \     |\  ___ \         |\   ___ \|\   __  \|\   __  \|\  \|\  \     
\ \  \___|\ \  \|\  \ \  \|\  \ \  \___|\ \  \    \ \   __/|        \ \  \_|\ \ \  \|\  \ \  \|\  \ \  \/  /|_   
 \ \  \  __\ \  \\\  \ \  \\\  \ \  \  __\ \  \    \ \  \_|/__       \ \  \ \\ \ \  \\\  \ \   _  _\ \   ___  \  
  \ \  \|\  \ \  \\\  \ \  \\\  \ \  \|\  \ \  \____\ \  \_|\ \       \ \  \_\\ \ \  \\\  \ \  \\  \\ \  \\ \  \ 
   \ \_______\ \_______\ \_______\ \_______\ \_______\ \_______\       \ \_______\ \_______\ \__\\ _\\ \__\\ \__\
    \|_______|\|_______|\|_______|\|_______|\|_______|\|_______|        \|_______|\|_______|\|__|\|__|\|__| \|__|
                                                                                                  
"""

print(ascii_art)

# Google Custom Search JSON API configuration
API_KEY = 'AIzaSyAG6NCqxDRnmxsVtCJG7MxEdjFSstRg__k'
CSE_ID = 'f6ea294506d68442d'
SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# List of Google dorks
dorks = [
    'site:tesla.com filetype:pdf',
    'intitle:"index of" site:tesla.com',
    'inurl:admin site:tesla.com',
    'filetype:sql site:tesla.com',
    # Add other dorks here...
]

def get_search_results(query):
    """Fetch the Google search results."""
    params = {
        'q': query,
        'key': API_KEY,
        'cx': CSE_ID
    }
    response = requests.get(SEARCH_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return {}

def main():
    output_file = "dork_results.txt"
    
    with open(output_file, "a") as outfile:
        for dork in dorks:
            print(f"Running dork: {dork}")
            results = get_search_results(dork)

            if 'items' in results:
                for item in results['items']:
                    title = item.get('title', 'No Title')
                    link = item.get('link', 'No Link')

                    print(title)
                    print(link)

                    outfile.write(title + "\n")
                    outfile.write(link + "\n")
                    outfile.write("-" * 50 + "\n")
            else:
                print("No results found or reached API limit!")

            # To avoid hitting the API rate limit, introduce a delay between requests
            time.sleep(20)

if __name__ == '__main__':
    main()
