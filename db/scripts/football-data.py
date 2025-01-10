import os
import requests
import sqlite3
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Leagues to filter
leagues = {'SA', 'PL', 'FL1', 'PD', 'BL1'}


def fetch_all_data():
    """
    Fetch all competition data from the API.
    """
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")

    url = 'http://api.football-data.org/v4/competitions'
    headers = {'X-Auth-Token': api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('competitions', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def filter_league_data(competitions):
    """
    Filter competition data for specified leagues and transform into usable format.
    """
    competitions_dict = {}

    for competition in competitions:
        code = competition.get('code')
        if code in leagues:
            name = competition.get('name')
            emblem = competition.get('emblem')
            area = competition.get('area', {})
            country_name = area.get('name')
            country_code = area.get('code')
            country_flag = area.get('flag')
            current_season = competition.get('currentSeason', {})
            start_date = current_season.get('startDate')
            end_date = current_season.get('endDate')
            num_weeks = pd.to_datetime(end_date) - pd.to_datetime(start_date) if start_date and end_date else None

            competitions_dict[code] = {
                'name': name,
                'emblem': emblem,
                'country_name': country_name,
                'country_code': country_code,
                'country_flag': country_flag,
                'num_weeks': num_weeks.days // 7 if num_weeks else None,
                'seasons': competition.get('seasons', [
                    {
                        'startDate' : start_date,
                        'endDate' : end_date
                    }
                ])
            }

    return competitions_dict


def store_leagues_in_db(competitions_dict):
    """
    Store league data in the Leagues table.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    league_ids = {}
    for code, league_data in competitions_dict.items():
        cursor.execute("""
            INSERT INTO Leagues (name, code, emblem, country, country_code, country_flag, num_weeks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            league_data['name'],
            code,
            league_data['emblem'],
            league_data['country_name'],
            league_data['country_code'],
            league_data['country_flag'],
            league_data['num_weeks']
        ))
        league_ids[code] = cursor.lastrowid  # Store the auto-generated league_id

    conn.commit()
    conn.close()

    return league_ids


def store_seasons_in_db(league_ids, competitions_dict):
    """
    Store season data for all leagues in the Seasons table.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for code, league_data in competitions_dict.items():
        league_id = league_ids.get(code)
        if league_id:
            for season in league_data.get('seasons', []):
                year = f"{pd.to_datetime(season['startDate']).year}-{pd.to_datetime(season['endDate']).year}"
                cursor.execute("""
                    INSERT INTO Seasons (league_id, year, start_date, end_date)
                    VALUES (?, ?, ?, ?)
                """, (
                    league_id,
                    year,
                    season.get('startDate'),
                    season.get('endDate')
                ))

    conn.commit()
    conn.close()


def fetch_and_store_leagues_and_seasons():
    """
    Main function to fetch competition data, process it, and store it into the database.
    """
    # Step 1: Fetch data
    competitions = fetch_all_data()

    # Step 2: Filter data for specified leagues
    competitions_dict = filter_league_data(competitions)
    print("Filtered Competitions Data:", competitions_dict)

    # Step 3: Store leagues and retrieve their IDs
    league_ids = store_leagues_in_db(competitions_dict)

    # Step 4: Store seasons linked to leagues
    store_seasons_in_db(league_ids, competitions_dict)


if __name__ == "__main__":
    fetch_and_store_leagues_and_seasons()
