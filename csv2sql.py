import os
import pandas as pd
import sqlite3

def convert_csv2sql():

    dbfile = "database.db"  # db file name
    dbname = "Players"      # name of database used in querying
    csv_dir = "teamDatabase"  # local directory next to the Python files

    conn = sqlite3.connect(dbfile)  

    # adds all csv files into the SQL database

    for league in os.listdir(csv_dir):          
        path = os.path.join(csv_dir, league)
        for team in (os.listdir(path)):
            team_path = os.path.join(path, team)
            try:
                df = pd.read_csv(team_path)
                df['FantasyUser'] = None    # adds a column to assign player to a fantasy user's team
                df.to_sql(name=dbname, con=conn, if_exists='replace', index=False)
                #team_name = os.path.splitext(team)[0]
                #print(f"[DEBUG] Completed conversion for team: {team_name}")
            except Exception as e:
                print(f"!!!CURCIAL ERROR!!! Unable to add to database! Error code: {e}")

    conn.close()

# Uncomment this to run file
convert_csv2sql()