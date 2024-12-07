import os
import pandas as pd
import sqlite3

def convert_csv2sql():

    dbfile = "database.db"
    dbname = "Players"
    csv_dir = r"D:\Taiki\Desktop\CS_Projects\fantasy\teamDatabase"

    conn = sqlite3.connect(dbfile)

    for league in os.listdir(csv_dir):
        path = os.path.join(csv_dir, league)
        for team in (os.listdir(path)):
            team_path = os.path.join(path, team)
            try:
                df = pd.read_csv(team_path)
                df.to_sql(name=dbname, con=conn, if_exists='replace', index=False)
                #team_name = os.path.splitext(team)[0]
                #print(f"[DEBUG] Completed conversion for team: {team_name}")
            except Exception as e:
                print(f"!!!CURCIAL ERROR!!! Unable to add to database! Error code: {e}")

    conn.close()