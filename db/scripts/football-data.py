import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

def fetch_competition_data(competition_code='PL'):
    """
    Fetch competition data from football-data.org and save to JSON file
    Args:
        competition_code (str): Competition code (e.g., 'PL' for Premier League)
    """
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")

    url = f'http://api.football-data.org/v4/competitions/{competition_code}'
    headers = {
        'X-Auth-Token': api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Save to JSON file
        output_file = 'scripts/dump_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Data saved to {output_file}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    fetch_competition_data()