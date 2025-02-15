import requests
import json
from datetime import datetime
import os

# ASCII Art Title
ascii_art = """
$$$$$$$$\ $$\   $$\ $$$$$$$\  $$$$$$$$\  $$$$$$\ $$$$$$$$\       $$$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  
\__$$  __|$$ |  $$ |$$  __$$\ $$  _____|$$  __$$\\__$$  __|      $$  _____|$$  _____|$$  _____|$$  __$$\ 
   $$ |   $$ |  $$ |$$ |  $$ |$$ |      $$ /  $$ |  $$ |         $$ |      $$ |      $$ |      $$ |  $$ |
   $$ |   $$$$$$$$ |$$$$$$$  |$$$$$\    $$$$$$$$ |  $$ |         $$$$$\    $$$$$\    $$$$$\    $$ |  $$ |
   $$ |   $$  __$$ |$$  __$$< $$  __|   $$  __$$ |  $$ |         $$  __|   $$  __|   $$  __|   $$ |  $$ |
   $$ |   $$ |  $$ |$$ |  $$ |$$ |      $$ |  $$ |  $$ |         $$ |      $$ |      $$ |      $$ |  $$ |
   $$ |   $$ |  $$ |$$ |  $$ |$$$$$$$$\ $$ |  $$ |  $$ |         $$ |      $$$$$$$$\ $$$$$$$$\ $$$$$$$  |
   \__|   \__|  \__|\__|  \__|\________|\__|  \__|  \__|         \__|      \________|\________|\_______/
"""

print(ascii_art)

def fetch_news(api_url, params):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_file(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

if __name__ == "__main__":
    # Define APIs and parameters
    news_api_key = os.getenv("NEWS_API_KEY")
    if not news_api_key:
        print("Error: NEWS_API_KEY environment variable not set.")
        exit(1)

    cybersecurity_url = "https://newsapi.org/v2/everything"
    international_news_url = "https://newsapi.org/v2/top-headlines"
    stock_market_news_url = "https://newsapi.org/v2/everything"

    current_date = datetime.now().strftime('%Y-%m-%d')
    output_file = f"threat_intelligence_feed_{current_date}.json"

    # Parameters for each category
    cybersecurity_params = {
        "q": "cybersecurity",
        "from": current_date,
        "sortBy": "publishedAt",
        "apiKey": news_api_key
    }

    international_news_params = {
        "category": "general",
        "language": "en",
        "apiKey": news_api_key
    }

    stock_market_news_params = {
        "q": "stock market OR finance investing",
        "from": current_date,
        "sortBy": "publishedAt",
        "apiKey": news_api_key
    }

    # Fetch data
    print("Fetching cybersecurity news...")
    cybersecurity_news = fetch_news(cybersecurity_url, cybersecurity_params)

    print("Fetching international news...")
    international_news = fetch_news(international_news_url, international_news_params)

    print("Fetching stock market and finance news...")
    stock_market_news = fetch_news(stock_market_news_url, stock_market_news_params)

    # Consolidate data
    threat_intelligence_feed = {
        "date": current_date,
        "cybersecurity_news": cybersecurity_news.get("articles", []) if cybersecurity_news else [],
        "international_news": international_news.get("articles", []) if international_news else [],
        "stock_market_news": stock_market_news.get("articles", []) if stock_market_news else []
    }

    # Save to file
    save_to_file(threat_intelligence_feed, output_file)