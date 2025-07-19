from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = "https://sportsbook.draftkings.com/leagues/baseball/mlb"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
tables = soup.find_all('table')

combined_rows = []


def convertAmericanToDec(strOdds):
    if strOdds:
        odds = int(strOdds.replace('−', '-').replace('+', ''))
        if odds > 0:
            return float(1 + (odds/100)) 
        else:
            return float(1 + (100 / abs(odds)))
    else:
        return None

for table in tables:
    rows = table.find_all('tr')

    for row in rows:
        th = row.find('th')
        if not th:
            continue  # skip extra rows
        
        # extract team name
        team_name_tag = th.find('div', class_ = "event-cell__name-text")
        if team_name_tag:
            team_name = team_name_tag.get_text(strip=True)
        else:
            team_name = th.get_text(strip=True)

        # clean odds data
        td_elements = row.find_all('td')
        odds = [td.get_text(strip=True).replace('\xa0', ' ') for td in td_elements]

        if odds:
            combined_rows.append([team_name] + odds)


games = []

for i in range(0, len(combined_rows), 2):
    try:
        # home and away teams
        away = combined_rows[i]
        home = combined_rows[i + 1]

        # team names
        away_team = away[0]
        home_team = home[0]

        # helper func to parse through spread
        # ex input: "-5.5+108" or "+5.5−140"
        def parse_spread(spread_str):
            # regex to split points (including + or - and decimal) and odds (with sign)
            match = re.match(r'([+-]?\d+(\.\d+)?)([+\-−]\d+)', spread_str)
            if match:
                pts = match.group(1)
                odds = match.group(3).replace('−', '-')  # normalize minus sign
                return pts, odds
            else:
                return None, None

        away_spread_pts, away_spread_odds = parse_spread(away[1])
        home_spread_pts, home_spread_odds = parse_spread(home[1])

        # extract totals from one row (usually both same)
        # ex: "O9.5−102" or "U9.5−127"
        def parse_total(total_str):
            import re
            # "O" or "U" followed by points and odds
            match = re.match(r'([OU])(\d+(\.\d+)?)([+\-−]\d+)', total_str)
            if match:
                side = match.group(1)  # O or U
                pts = match.group(2)
                odds = match.group(4).replace('−', '-')
                return side, pts, odds
            else:
                return None, None, None

        total_over_side, total_pts_over, total_over_odds = parse_total(away[2])
        total_under_side, total_pts_under, total_under_odds = parse_total(home[2])

        total_pts = total_pts_over or total_pts_under

        # moneyline odds
        away_moneyline = away[3] if len(away) > 3 else None
        home_moneyline = home[3] if len(home) > 3 else None

        game_data = {
            "TEAM_AWAY": away_team,
            "SPREAD_AWAY_PTS": away_spread_pts,
            "SPREAD_AWAY_ODDS": convertAmericanToDec(away_spread_odds),
            "TEAM_HOME": home_team,
            "SPREAD_HOME_PTS": home_spread_pts,
            "SPREAD_HOME_ODDS": convertAmericanToDec(home_spread_odds),
            "TOTAL_PTS": total_pts,
            "TOTAL_OVER_ODDS": convertAmericanToDec(total_over_odds),
            "TOTAL_UNDER_ODDS": convertAmericanToDec(total_under_odds),
            "MONEYLINE_AWAY": convertAmericanToDec(away_moneyline),
            "MONEYLINE_HOME": convertAmericanToDec(home_moneyline),
        }

        games.append(game_data)

    except IndexError:
        pass


# conv to pandas df and csv to use elsewhere
df = pd.DataFrame(games)
df.to_csv('draftkings_odds.csv', index=False)