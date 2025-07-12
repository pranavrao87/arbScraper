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
        '734.131552906',
        '734.131548191',
        '734.131552907',
        '734.131498713',
        '734.131422800',
        '734.131498716',
        '734.131498533',
        '734.131423001',
        '734.131498534',
        '734.131498953',
        '734.131422782',
        '734.131498950',
        '734.131499271',
        '734.131422856',
        '734.131499270',
        '734.131498778',
        '734.131422960',
        '734.131498780',
        '734.131499477',
        '734.131422779',
        '734.131499476',
        '734.131501546',
        '734.131422780',
        '734.131501543',
        '734.131501600',
        '734.131422783',
        '734.131501596',
        '734.131501442',
        '734.131423029',
        '734.131501449',
        '734.131501329',
        '734.131423035',
        '734.131501328',
        '734.131500944',
        '734.131422930',
        '734.131500949',
        '734.131500876',
        '734.131422851',
        '734.131500872',
        '734.131500642',
        '734.131422876',
        '734.131500637',
        '734.131500308',
        '734.131423021',
        '734.131500304',
        '734.131499735',
        '734.131423026',
        '734.131499737',
    ],
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

games = defaultdict(dict)

for market_id in odds_json['marketIds']:
    market = markets[market_id]
    event_id = str(market.get('eventId'))
    event_info = events.get(event_id)

    if event_info:
        matchup = event_info['name']
        parts = matchup.split(' @ ')
        away_team = parts[0].split(' (')[0]
        home_team = parts[1].split(' (')[0]
    else:
        matchup = "Unknown Matchup"

    print(f"Market: {market.get('marketName')} | Matchup: {home_team} @ {away_team}")
    for runner in market.get('runners', []):
        name = runner['runnerName']
        odds = runner['winRunnerOdds']['americanDisplayOdds']['americanOdds'] # Can switch out with ['decimalOdds']['decimalOdds']
        print(f"  {name}: {odds}")