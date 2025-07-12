from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pprint import pprint

odds_headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
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
    'x-application': 'FhMFpcPWXMeyZxOx',
    'x-px-context': '_px3=f5acce725b5ba3617c101f29ddf37a6cb6c69d06eb039fedb4b20ffc0910e90e:EvmfSiYcFepfI5hRSL2nDdC0zu0iJ5cveUecmvIR0bIcebEdImTzwaOhnbx1ecszkaCC34SPNFrASdZzfki/jw==:1000:vr1h+goHpFPyJMPJgVnyIMNwKXsyyEphB6hZjEIukG7pt0Yn4B2ROKJSOcsTa8dr7T8uyl7Xtd6J6+uC5/TNt61AIYWazD8UvDcBUl9WNrleJpT1tJq8wrEQKkMFu2VS4i6SkkWW8gqe136WDvJIe8M4hsMBBzuykuAkkVFHs0K6knRGP8AcKkO1vDUc08A5/4FOuf5x0gnsLqNiq39IVyCYS5nEl/pr9S65B/zdW48=;_pxvid=2d15317c-5bb2-11f0-99a0-31c8901a01b9;pxcts=2d15463f-5bb2-11f0-99a0-782caa133fd8;',
}

odds_params = {
    'priceHistory': '0',
}

# Have to update these constantly 
odds_json = {
   'marketIds': [
        '734.131700405',
        '734.131573861',
        '734.131700412',
        '734.131700622',
        '734.131573845',
        '734.131700623',
        '734.131633863',
        '734.131573850',
        '734.131633864',
        '734.131634161',
        '734.131573848',
        '734.131634158',
        '734.131634019',
        '734.131573872',
        '734.131634021',
        '734.131634547',
        '734.131573846',
        '734.131634552',
        '734.131634775',
        '734.131573851',
        '734.131634778',
        '734.131634428',
        '734.131573855',
        '734.131634434',
        '734.131667087',
        '734.131573859',
        '734.131667094',
        '734.131634293',
        '734.131573870',
        '734.131634290',
        '734.131634855',
        '734.131573854',
        '734.131634850',
        '734.131635175',
        '734.131573873',
        '734.131635178',
        '734.131635268',
        '734.131573862',
        '734.131635265',
        '734.131635481',
        '734.131573838',
        '734.131635489',
        '734.131763502',
        '734.131709198',
        '734.131763499',
        '734.131763391',
        '734.131709199',
        '734.131763396',
        '734.131763632',
        '734.131709219',
        '734.131763633',
        '734.131763960',
        '734.131709212',
        '734.131763959',
        '734.131763847',
        '734.131709213',
        '734.131763851',
        '734.131764141',
        '734.131709190',
        '734.131764136',
        '734.131764067',
        '734.131709194',
        '734.131764061',
        '734.131764097',
        '734.131709195',
        '734.131764099',
        '734.131764220',
        '734.131709197',
        '734.131764222',
        '734.131763985',
   ]
}

odds_response = requests.post(
    'https://smp.nj.sportsbook.fanduel.com/api/sports/fixedodds/readonly/v1/getMarketPrices',
    params=odds_params,
    headers=odds_headers,
    json=odds_json,
)

rawData = odds_response.json()

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

# Define dictionary where the key is the tuple (home_team, away_team) and it links to the fields of the diff bets and odds
games = {}

for market_id in odds_json['marketIds']:
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
        name = runner['runnerName']
        odds = runner['winRunnerOdds']['americanDisplayOdds']['americanOdds']

        if bet_type == "Moneyline":
            if name == away_team:
                games[match_key]["MONEYLINE_AWAY"] = odds
            elif name == home_team:
                games[match_key]["MONEYLINE_HOME"] = odds
        elif bet_type == "Run Line":
            pts = runner["handicap"]
            if name == away_team:
                games[match_key]["SPREAD_AWAY_ODDS"] = odds
                games[match_key]["SPREAD_AWAY_PTS"] = pts
            elif name == home_team:
                games[match_key]["SPREAD_HOME_ODDS"] = odds
                games[match_key]["SPREAD_HOME_PTS"] = pts
        elif bet_type == "Total Runs":
            total = runner["handicap"]
            games[match_key]["TOTAL_PTS"] = total
            if name == "Over":
                games[match_key]["TOTAL_OVER_ODDS"] = odds
            elif name == "Under":
                games[match_key]["TOTAL_UNDER_ODDS"] = odds
        
df = pd.DataFrame(games.values())
print(df)