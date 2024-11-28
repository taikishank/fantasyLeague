import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
import os

#   dataset() function
#   no param
#   scrapes fbref for player data for each top 5 league team
#   stores infromation into csv file
#   csv files used in SQL database for easy querying



def dataset():

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
#   csv file dependent upon the league
#   ex  Barcelona is in La_Liga, Tottenham is in Premier_League, etc...

    counter = 0

    for link in team_urls:
        # if (link == "https://fbref.com/en/squads/206d90db/Barcelona-Stats"):
        #     continue
        team_name = link.split("/")[-1].replace("Stats", "").replace("-", " ")
        data = requests.get(link)

        try:
            players = pd.read_html(StringIO(data.text), match="Standard Stats")[0]
            players.columns = players.columns.droplevel()
        except ValueError:
            print("Error trying to pass over table for " + team_name)
            pass

        
        players = players.loc[:, ~players.columns.duplicated()]
        player_data = players[['Player', 'Pos', 'Age', 'MP', 'Min', 'Gls', 'Ast', 'CrdY', 'CrdR', 'xG', 'xAG']]     #   relevant categories for data
        player_data = player_data[:-2]      #   last two rows are total team stats, not necessary for this program

    #   many different instances of '/en/comps/', grab the second instance as it is easiest to extract league name
    #   store datatable into csv

        soup = BeautifulSoup(requests.get(link).text, features="lxml")
        league = soup.find_all('a', href=lambda href: href and '/en/comps/' in href)[1]
        league = league.text.replace(' ', '_')
        player_data = pd.DataFrame(data = data)
        folder_path = r"D:\Taiki\Desktop\CS_Projects\premierLeagueWebScrape\teamDatabase"
        player_data.to_csv(folder_path + '\\' + league + '\\' + team_name, index=False)

        print(team_name + " successfully uploaded as csv to " + league)
        time.sleep(10)   # sleep so fbref gods dont ban

        # if (counter == 4):
        #     break
        # counter += 1