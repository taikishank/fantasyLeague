import os
import json
import requests
import sqlite3
from dotenv import load_dotenv
import pprint as pp

# Load environment variables from .env file
load_dotenv()

leagues = {'SA', 'PL', 'FL1', 'PD', 'BL1'}

def fetch_competitions():
    """
    Fetch competition data for leagues specified in the leagues set.
    """
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")

    url = 'http://api.football-data.org/v4/competitions'
    headers = {'X-Auth-Token': api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Create a filtered dictionary mapping codes to league names and emblems
        competitions_dict = {}
        for competition in data.get('competitions', []):
            code = competition['code']
            if code in leagues:  # Only include leagues that are in our set
                name = competition['name']
                emblem = competition.get('emblem', None)

                area = competition.get('area', None)
                country_name = area.get('name', None)
                country_code = area.get('code', None)
                country_flag = area.get('flag', None)

                competitions_dict[code] = {'name': name, 'emblem': emblem, 'country_name' : country_name, 'country_code' : country_code, 'country_flag' : country_flag}

        # Save competitions to the database
        store_leagues_in_db(competitions_dict)
        
        return competitions_dict

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

def store_leagues_in_db(competitions_dict):
    """
    Store league and area data into the database.
    Args:
        competitions_dict (dict): Filtered competition data with league details.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for code, league_data in competitions_dict.items():
        # Insert data into the Leagues table
        cursor.execute("""
            INSERT INTO Leagues (name, code, emblem, country, country_code, country_flag, number_of_weeks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            league_data['name'],          # League name
            code,                         # League code
            league_data['emblem'],        # League emblem
            league_data['country_name'],  # Country name
            league_data['country_code'],  # Country code
            league_data['country_flag'],  # Country flag
            38                            # Default number of weeks
        ))
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    competitions_dict = fetch_competitions()
    pp.pprint(competitions_dict)