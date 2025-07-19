import pandas as pd
from utilFuncs import decimalToAmerican
from pprint import pprint

df_dk = pd.read_csv('draftkings_odds.csv')
df_fd = pd.read_csv('fanduel_odds.csv')
df_espn = pd.read_csv('espn_odds.csv')

# helper function to calculate optimal betting amount based on arb/odds
def calculate_arb_bets(odds1, odds2, total_stake=100):
    b1 = total_stake / ((odds1 / odds2) + 1)
    b2 = total_stake - b1
    payout = round(b1 * odds1, 2)
    profit = round(payout - total_stake, 2)
    return round(b1, 2), round(b2, 2), payout, profit

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

for _, row_dk in df_dk.iterrows():
    home = row_dk['TEAM_HOME']
    away = row_dk['TEAM_AWAY']
    
    # find a matching row in FanDuel
    match_fd = df_fd[(df_fd['TEAM_HOME'] == home) & (df_fd['TEAM_AWAY'] == away)]
    match_espn = df_espn[(df_espn['TEAM_HOME'] == home) & (df_espn['TEAM_AWAY'] == away)]

    # Gather all available odds in a dict: {source: (home_odds, away_odds)}
    odds_sources = {}

    # DraftKings odds (assumed decimal)
    dk_home = row_dk['MONEYLINE_HOME']
    dk_away = row_dk['MONEYLINE_AWAY']
    odds_sources['DraftKings'] = (dk_home, dk_away)

    # FanDuel odds if available
    if not match_fd.empty:
        fd_home = match_fd.iloc[0]['MONEYLINE_HOME']
        fd_away = match_fd.iloc[0]['MONEYLINE_AWAY']
        odds_sources['FanDuel'] = (fd_home, fd_away)

    # ESPN odds if available
    if not match_espn.empty:
        espn_home = match_espn.iloc[0]['MONEYLINE_HOME']
        espn_away = match_espn.iloc[0]['MONEYLINE_AWAY']
        odds_sources['ESPN'] = (espn_home, espn_away)

    # Find best home and away odds and source
    best_home_source, best_home_pair = max(odds_sources.items(), key=lambda x: x[1][0])
    best_home_odds = best_home_pair[0]

    best_away_source, best_away_pair = max(odds_sources.items(), key=lambda x: x[1][1])
    best_away_odds = best_away_pair[1]

    inv_sum = 1 / best_home_odds + 1 / best_away_odds

    if inv_sum < 1:
        print(f"Arbitrage Found: {away} @ {home}")
        print(f" Best Home ML: {best_home_odds:.2f} (Decimal) from {best_home_source} | American: {decimalToAmerican(best_home_odds)}")
        print(f" Best Away ML: {best_away_odds:.2f} (Decimal) from {best_away_source} | American: {decimalToAmerican(best_away_odds)}")
        print(f" Implied Probability Sum: {inv_sum:.3f}")
        b1, b2, payout, profit = calculate_arb_bets(best_home_odds, best_away_odds)
        print(f" Optimal Betting, Home:{b1}, Away:{b2}, Payout:{payout}, Profit:{profit}\n")
    
    # Total points O/U Lines
    totals_odds = {}

    # DraftKings totals
    if not pd.isna(row_dk['TOTAL_PTS']):
        dk_line = row_dk['TOTAL_PTS']
        dk_over = row_dk['TOTAL_OVER_ODDS']
        dk_under = row_dk['TOTAL_UNDER_ODDS']
        totals_odds['DraftKings'] = (dk_line, dk_over, dk_under)

    if not match_fd.empty and not pd.isna(match_fd.iloc[0]['TOTAL_PTS']):
        fd_line = match_fd.iloc[0]['TOTAL_PTS']
        fd_over = match_fd.iloc[0]['TOTAL_OVER_ODDS']
        fd_under = match_fd.iloc[0]['TOTAL_UNDER_ODDS']
        totals_odds['FanDuel'] = (fd_line, fd_over, fd_under)

    if not match_espn.empty and not pd.isna(match_espn.iloc[0]['TOTAL_PTS']):
        espn_line = match_espn.iloc[0]['TOTAL_PTS']
        espn_over = match_espn.iloc[0]['TOTAL_OVER_ODDS']
        espn_under = match_espn.iloc[0]['TOTAL_UNDER_ODDS']
        totals_odds['ESPN'] = (espn_line, espn_over, espn_under)

    # Find arbitrage opportunities on totals (only if all lines match)
    over_odds_list = []
    under_odds_list = []
    lines_seen = set()

    for source, (line, over, under) in totals_odds.items():
        lines_seen.add(line)
        over_odds_list.append((source, over))
        under_odds_list.append((source, under))

    if len(lines_seen) == 1:  # Make sure they are for the same line
        best_over_source, best_over_odds = max(over_odds_list, key=lambda x: x[1])
        best_under_source, best_under_odds = max(under_odds_list, key=lambda x: x[1])

        inv_total = 1 / best_over_odds + 1 / best_under_odds

        if inv_total < 1:
            print(f"--- TOTAL POINTS ARBITRAGE (Line: {lines_seen.pop()}) ---")
            print(f"{away} @ {home}")
            print(f" Best OVER:  {best_over_odds:.2f} from {best_over_source} | American: {decimalToAmerican(best_over_odds)}")
            print(f" Best UNDER: {best_under_odds:.2f} from {best_under_source} | American: {decimalToAmerican(best_under_odds)}")
            print(f" Implied Probability Sum: {inv_total:.3f}")
            b1, b2, payout, profit = calculate_arb_bets(best_over_odds, best_under_odds)
            print(f" Optimal Betting, Over:{b1:.2f}, Under:{b2:.2f}, Payout:{payout:.2f}, Profit:{profit:.2f}\n")