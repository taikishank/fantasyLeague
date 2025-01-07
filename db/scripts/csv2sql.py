import os
import pandas as pd
from pathlib import Path
from ..database import get_connection

def convert_csv2sql():
    dbname = "Players"      # name of database used in querying
    csv_dir = Path(__file__).parent.parent.parent / "teamDatabase"  # adjust path relative to script location

    conn = get_connection()

    for league in os.listdir(csv_dir):          
        path = os.path.join(csv_dir, league)
        for team in (os.listdir(path)):
            team_path = os.path.join(path, team)
            try:
                df = pd.read_csv(team_path)
                df['FantasyUser'] = None    
                df.to_sql(name=dbname, con=conn, if_exists='replace', index=False)
            except Exception as e:
                print(f"!!!CRUCIAL ERROR!!! Unable to add to database! Error code: {e}")

    conn.close()

if __name__ == "__main__":
    convert_csv2sql()