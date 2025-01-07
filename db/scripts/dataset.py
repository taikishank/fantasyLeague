import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
import os
from pathlib import Path

#   dataset() function
#   no param
#   scrapes fbref for player data for each top 5 league team
#   stores infromation into csv file
#   csv files used in SQL database for easy querying

def dataset():
    # Define base directory for data storage
    base_dir = Path(__file__).parent.parent.parent
    team_database_dir = base_dir / "teamDatabase"
    
    #   use BeautifulSoup to extract the main Big-5 table with all teams from top 5 leagues

    url = "https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats"
    data = requests.get(url)
    time.sleep(4)
    soup = BeautifulSoup(data.text, features="lxml")
    standings_table = soup.select('table.stats_table')[0]
    links = standings_table.find_all('a')
    links = [l.get("href") for l in links]
    squad_links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in squad_links]

    #   iterates through each team url and extracts the team name and leauge
    #   extracts respective data table and converts to csv 
    #   csv file directory dependent upon the league
    #   ex  Barcelona is in La_Liga, Tottenham is in Premier_League, etc...

    for link in team_urls:
        team_name = link.split("/")[-1].replace("Stats", "").replace("-", " ")
        data = requests.get(link)

        try:
            players = pd.read_html(StringIO(data.text), match="Standard Stats")[0]
            players.columns = players.columns.droplevel()
        except ValueError:
            print("!!!CRUCIAL ERROR!!! Error trying to pass over table for " + team_name)
            pass
        
        players = players.loc[:, ~players.columns.duplicated()]
        player_data = players[['Player', 'Pos', 'Age', 'MP', 'Min', 'Gls', 'Ast', 'CrdY', 'CrdR', 'xG', 'xAG']]     #   relevant categories for data
        player_data = player_data[:-2]      #   last two rows are total team stats, not necessary for this program
        team_name = team_name[:-1]
        player_data['Club'] = team_name
        

    #   many different instances of '/en/comps/', grab the second instance as it is easiest to extract league name
    #   store datatable into csv

        soup = BeautifulSoup(requests.get(link).text, features="lxml")
        league = soup.find_all('a', href=lambda href: href and '/en/comps/' in href)[1]
        league = league.text.replace(' ', '_')
        player_data['League'] = league
        folder_path = team_database_dir
        league_path = folder_path / league
        league_path.mkdir(parents=True, exist_ok=True)
        
        file_path = league_path / f"{team_name.replace(' ', '_')}.csv"
        player_data.to_csv(file_path, index=False)
        
        print(f"{team_name} successfully uploaded as csv to {league}")
        time.sleep(10)   # sleep so fbref gods dont ban

if __name__ == "__main__":
    dataset()