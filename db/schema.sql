CREATE TABLE Leagues (
    league_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT,
    number_of_weeks INTEGER
);

CREATE TABLE Seasons (
    season_id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER NOT NULL,
    year TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    FOREIGN KEY (league_id) REFERENCES Leagues (league_id)
);

CREATE TABLE Weeks (
    week_id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    start_date TEXT,
    end_date TEXT,
    FOREIGN KEY (season_id) REFERENCES Seasons (season_id)
);

CREATE TABLE Teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (league_id) REFERENCES Leagues (league_id)
);

CREATE TABLE Players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    position TEXT,
    date_of_birth TEXT,
    nationality TEXT,
    FOREIGN KEY (team_id) REFERENCES Teams (team_id)
);

CREATE TABLE PlayerStats (
    player_stats_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    week_id INTEGER NOT NULL,
    goals_scored INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    minutes_played INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    fantasy_points INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES Players (player_id),
    FOREIGN KEY (week_id) REFERENCES Weeks (week_id)
);
