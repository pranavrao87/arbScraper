import requests
from pprint import pprint
import pandas as pd
from utilFuncs import convertAmericanIntToDec, convertAmericanStrToDec

URL = "https://site.web.api.espn.com/apis/personalized/v2/scoreboard/header"
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.espn.com',
    'priority': 'u=1, i',
    'referer': 'https://www.espn.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

params = {
    'sport': 'baseball',
    'league': 'mlb',
    'region': 'us',
    'lang': 'en',
    'contentorigin': 'espn',
    'configuration': 'SITE_DEFAULT',
    'platform': 'web',
    'buyWindow': '1m',
    'showAirings': 'buy,live,replay',
    'showZipLookup': 'true',
    'tz': 'America/New_York',
    'postalCode': '78729',
    'playabilitySource': 'playbackId',
}

response = requests.get(URL, params=params, headers=headers)
data = response.json()

game_list = []

# A list of "game" objects which each contain a bunch of data including odds
games = data['sports'][0]['leagues'][0]['events']

for game in games:
    name = game['name'] 
    
    home_odds = game['odds']['homeTeamOdds']
    away_odds = game['odds']['awayTeamOdds']

    # Points
    total_pts = game['odds']['overUnder']

    # Names 
    home_team = home_odds['team']['displayName']
    away_team = away_odds['team']['displayName']

    # Moneyline
    home_moneyline = home_odds['moneyLine']
    away_moneyline = away_odds['moneyLine']

    # Spread
    home_spread_odds = game['odds']['pointSpread']['home']['close']['odds']
    home_spread_pts = game['odds']['pointSpread']['home']['close']['line']
    away_spread_odds = game['odds']['pointSpread']['away']['close']['odds']
    away_spread_pts = game['odds']['pointSpread']['away']['close']['line']

    # Over/Under
    total_over_odds = game['odds']['overOdds']
    total_under_odds = game['odds']['underOdds']

    game_data = {
        "TEAM_AWAY": away_team,
        "SPREAD_AWAY_PTS": away_spread_pts,
        "SPREAD_AWAY_ODDS": convertAmericanStrToDec(away_spread_odds),
        "TEAM_HOME": home_team,
        "SPREAD_HOME_PTS": home_spread_pts,
        "SPREAD_HOME_ODDS": convertAmericanStrToDec(home_spread_odds),
        "TOTAL_PTS": total_pts,
        "TOTAL_OVER_ODDS": convertAmericanIntToDec(total_over_odds),
        "TOTAL_UNDER_ODDS": convertAmericanIntToDec(total_under_odds),
        "MONEYLINE_AWAY": convertAmericanIntToDec(away_moneyline),
        "MONEYLINE_HOME": convertAmericanIntToDec(home_moneyline),
    }

    game_list.append(game_data)

df = pd.DataFrame(game_list)
df.to_csv('espn_odds.csv', index=False)