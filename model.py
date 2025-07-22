import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from pprint import pprint 
from io import StringIO



# team standings data for 2025 season (the table is wrapped inside a comment)
standings_url = "https://www.baseball-reference.com/leagues/MLB-standings.shtml"
response1 = requests.get(standings_url)
soup1 = BeautifulSoup(response1.text, "html.parser")

comments1 = soup1.find_all(string=lambda text: isinstance(text, Comment))

for comment1 in comments1:
    if 'expanded_standings_overall' in comment1:
        commented_soup1 = BeautifulSoup(comment1, "html.parser")
        table = commented_soup1.find("table", {"id": "expanded_standings_overall"})
        if table:
            df_standings = pd.read_html(StringIO(str(table)))[0]
            print("=== Team Standings ===")
            print(df_standings.head())
            break

# team batting stats for 2025 season
stats_url = "https://www.baseball-reference.com/leagues/majors/2025.shtml"
response2 = requests.get(stats_url)
soup2 = BeautifulSoup(response2.text, "html.parser")

table_batting = soup2.find("table", {"id": "teams_standard_batting"})
df_batting = pd.read_html(StringIO(str(table_batting)))[0]
print("=== Team Batting Stats ===")
print(df_batting.head())

# team pitching stats for 2025 season (this table is nested in a comment)
comments2 = soup2.find_all(string=lambda text: isinstance(text, Comment))
for comment in comments2:
    if 'teams_standard_pitching' in comment:
        commented_soup2 = BeautifulSoup(comment, "html.parser")
        table_pitching = commented_soup2.find("table", {"id": "teams_standard_pitching"})
        if table_pitching:
            df_pitching = pd.read_html(StringIO(str(table_pitching)))[0]
            print("=== Team Pitching Stats ===")
            print(df_pitching.head())
            break

"""
What stats do I want to use to predict outcomes?
- for now start w/ a few basic features:
    - Current record (W/L)
    - Last 10 games
    - Home/away performance
    - R/G and RA/G --> runs / game and runs allowed / game
"""

# Get a dataframe of odds just for the current matchups/games to predict on
df_espn = pd.read_csv('espn_odds.csv')


for _, game in df_espn.iterrows():
    homeTeam = game["TEAM_HOME"]
    awayTeam = game["TEAM_AWAY"]

    # Get the matching rows for the home and away teams from standings, pitching, and batting tables
    standings_home_row = df_standings[(df_standings["Tm"] == homeTeam)]
    standings_away_row = df_standings[(df_standings["Tm"] == awayTeam)]

    batting_home_row = df_batting[(df_standings["Tm"] == homeTeam)]
    batting_away_row = df_batting[(df_standings["Tm"] == awayTeam)]

    pitching_home_row = df_pitching[(df_standings["Tm"] == homeTeam)]
    pitching_away_row = df_pitching[(df_standings["Tm"] == awayTeam)]


