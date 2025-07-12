import requests
import pandas as pd

marketID_headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'if-none-match': 'W/"11ce13-5xCVuxisUaSTxA2HAV7Jcy01rJc"',
    'origin': 'https://sportsbook.fanduel.com',
    'priority': 'u=1, i',
    'referer': 'https://sportsbook.fanduel.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-px-context': '_px3=f5acce725b5ba3617c101f29ddf37a6cb6c69d06eb039fedb4b20ffc0910e90e:EvmfSiYcFepfI5hRSL2nDdC0zu0iJ5cveUecmvIR0bIcebEdImTzwaOhnbx1ecszkaCC34SPNFrASdZzfki/jw==:1000:vr1h+goHpFPyJMPJgVnyIMNwKXsyyEphB6hZjEIukG7pt0Yn4B2ROKJSOcsTa8dr7T8uyl7Xtd6J6+uC5/TNt61AIYWazD8UvDcBUl9WNrleJpT1tJq8wrEQKkMFu2VS4i6SkkWW8gqe136WDvJIe8M4hsMBBzuykuAkkVFHs0K6knRGP8AcKkO1vDUc08A5/4FOuf5x0gnsLqNiq39IVyCYS5nEl/pr9S65B/zdW48=;_pxvid=2d15317c-5bb2-11f0-99a0-31c8901a01b9;pxcts=2d15463f-5bb2-11f0-99a0-782caa133fd8;',
}

marketID_params = {
    'page': 'CUSTOM',
    'customPageId': 'mlb',
    'pbHorizontal': 'false',
    '_ak': 'FhMFpcPWXMeyZxOx',
    'timezone': 'America/New_York',
}

marketID_response = requests.get('https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page', params=marketID_params, headers=marketID_headers)

data = marketID_response.json()

markets = data['attachments']['markets']
events = data['attachments']['events']

valid_market_names = {"Moneyline", "Run Line", "Total Runs"}

market_ids = []

for market_id, market in markets.items():
    name = market.get('marketName')
    status = market.get('marketStatus')

    if name in valid_market_names and status == 'OPEN':
        market_ids.append(market_id)


# Define dictionary where the key is the tuple (home_team, away_team) and it links to the fields of the diff bets and odds
games = {}

def update_game_odds(games, match_key, bet_type, runner, home_team, away_team):
    name = runner['runnerName']
    odds = runner['winRunnerOdds']['americanDisplayOdds']['americanOdds']
    pts = runner.get("handicap", None)

    if bet_type == "Moneyline":
        if name == away_team:
            games[match_key]["MONEYLINE_AWAY"] = odds
        elif name == home_team:
            games[match_key]["MONEYLINE_HOME"] = odds
    elif bet_type == "Run Line":
        if name == away_team:
            games[match_key]["SPREAD_AWAY_ODDS"] = odds
            games[match_key]["SPREAD_AWAY_PTS"] = pts
        elif name == home_team:
            games[match_key]["SPREAD_HOME_ODDS"] = odds
            games[match_key]["SPREAD_HOME_PTS"] = pts
    elif bet_type == "Total Runs":
        if pts is not None:
            games[match_key]["TOTAL_PTS"] = pts
        if name == "Over":
            games[match_key]["TOTAL_OVER_ODDS"] = odds
        elif name == "Under":
            games[match_key]["TOTAL_UNDER_ODDS"] = odds

for market_id in market_ids:
    market = markets[market_id]
    event_id = str(market.get('eventId'))
    event_info = events.get(event_id)
    if not event_info:
        continue  # or log error

    bet_type = market['marketName']
    matchup = event_info['name']

    parts = matchup.split(' @ ')
    away_team = parts[0].split(' (')[0]
    home_team = parts[1].split(' (')[0]
    match_key = (home_team, away_team)

    games.setdefault(match_key, {
        "TEAM_AWAY": away_team,
        "TEAM_HOME": home_team
    })

    for runner in market.get('runners', []):
        update_game_odds(games, match_key, bet_type, runner, home_team, away_team)


# Convert Dictionary to pd df
df = pd.DataFrame(games.values())