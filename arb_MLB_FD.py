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

odds_json = {
    'marketIds': [
        '734.131210983',
        '734.131138388',
        '734.131210972',
        '734.131211071',
        '734.131138308',
        '734.131211070',
        '734.131211099',
        '734.131138389',
        '734.131211095',
        '734.131376739',
        '734.131279849',
        '734.131376735',
        '734.131351441',
        '734.131279852',
        '734.131351442',
        '734.131352000',
        '734.131279831',
        '734.131352005',
        '734.131352172',
        '734.131279862',
        '734.131352173',
        '734.131383407',
        '734.131279854',
        '734.131383408',
        '734.131352206',
        '734.131279856',
        '734.131352211',
        '734.131352272',
        '734.131279836',
        '734.131352267',
        '734.131352322',
        '734.131279861',
        '734.131352326',
        '734.131352418',
        '734.131279851',
        '734.131352424',
        '734.131352473',
        '734.131279844',
        '734.131352466',
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

for market_id in odds_json['marketIds']:
    market = markets[market_id]
    event_id = str(market.get('eventId'))
    event_info = events.get(event_id)

    # Need to fix this part up
    # if event_info:
    #     home = event_info.get('homeTeam', 'Unknown')
    #     away = event_info.get('awayTeam', 'Unknown')
    #     matchup = f"{away} @ {home}"
    # else:
    #     matchup = "Unknown Matchup"

    print(f"Market: {market.get('marketName')} | Matchup: {matchup}")
    for runner in market.get('runners', []):
        name = runner['runnerName']
        odds = runner['winRunnerOdds']['americanDisplayOdds']['americanOdds']
        print(f"  {name}: {odds}")