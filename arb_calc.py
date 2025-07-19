import pandas as pd

df_dk = pd.read_csv('draftkings_odds.csv')
df_fd = pd.read_csv('fanduel_odds.csv')

# Draft Kings stores team names abbreviated so this mapping dict is necessary to match fanduel
team_name_map = {
    "ARI Diamondbacks": "Arizona Diamondbacks",
    "ATL Braves": "Atlanta Braves",
    "BAL Orioles": "Baltimore Orioles",
    "BOS Red Sox": "Boston Red Sox",
    "CHC Cubs": "Chicago Cubs",
    "CHW White Sox": "Chicago White Sox",
    "CIN Reds": "Cincinnati Reds",
    "CLE Guardians": "Cleveland Guardians",
    "COL Rockies": "Colorado Rockies",
    "DET Tigers": "Detroit Tigers",
    "HOU Astros": "Houston Astros",
    "KC Royals": "Kansas City Royals",
    "LAA Angels": "Los Angeles Angels",
    "LAD Dodgers": "Los Angeles Dodgers",
    "MIA Marlins": "Miami Marlins",
    "MIL Brewers": "Milwaukee Brewers",
    "MIN Twins": "Minnesota Twins",
    "NYM Mets": "New York Mets",
    "NY Yankees": "New York Yankees",
    "Athletics": "Athletics",
    "PHI Phillies": "Philadelphia Phillies",
    "PIT Pirates": "Pittsburgh Pirates",
    "SD Padres": "San Diego Padres",
    "SEA Mariners": "Seattle Mariners",
    "SF Giants": "San Francisco Giants",
    "STL Cardinals": "St Louis Cardinals",
    "TB Rays": "Tampa Bay Rays",
    "TEX Rangers": "Texas Rangers",
    "TOR Blue Jays": "Toronto Blue Jays",
    "WSH Nationals": "Washington Nationals"
}

df_dk['TEAM_HOME'] = df_dk['TEAM_HOME'].map(team_name_map)
df_dk['TEAM_AWAY'] = df_dk['TEAM_AWAY'].map(team_name_map)

# Loop through DraftKings DataFrame
for _, row_dk in df_dk.iterrows():
    home = row_dk['TEAM_HOME']
    away = row_dk['TEAM_AWAY']
    
    # Try to find a matching row in FanDuel
    match = df_fd[
        (df_fd['TEAM_HOME'] == home) & 
        (df_fd['TEAM_AWAY'] == away)
    ]

    if not match.empty:
        row_fd = match.iloc[0]
        
        # Collect all 4 odds
        dk_home = row_dk['MONEYLINE_HOME']
        dk_away = row_dk['MONEYLINE_AWAY']
        fd_home = row_fd['MONEYLINE_HOME']
        fd_away = row_fd['MONEYLINE_AWAY']

        # Check for arbitrage opportunities by comparing best odds from either book
        best_home = max(dk_home, fd_home)
        best_away = max(dk_away, fd_away)

        inv_sum = 1 / best_home + 1 / best_away

        if inv_sum < 1:
            print(f"  Arbitrage Found: {away} @ {home}")
            print(f"  Best Home ML: {best_home}")
            print(f"  Best Away ML: {best_away}")
            print(f"  Implied Probability Sum: {inv_sum:.3f}\n")
