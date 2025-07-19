# Arb Scraper Bot
A bot that scrapes live odds data from sportsbook sites and tries to figure out whether arbitrage opportunities exist or not
- currently only scrapes FanDuel, DraftKings, and ESPN for MLB odds

# To Run:
1. Give bash script permissons
```
chmod +x make_me_money.sh
```

2. Run bash script
```
./make_me_money
```

# The Process
Arbitrage is the idea of utilizing pricing differences across different markets to make risk free bets. In this case I utilize the different odds offered by various sports books such as ESPN, FanDuel, and DraftKings. I then parse through the odds (just moneyline odds for now), converting them from American to Decimal format to standardize them, and find which book is offering the best odds for each team in each matchup. For each game or matchup, I check whether the sum of the implied probabilities (1 / decimal odds) for both teams is less than 1. If it is, that signals a potential arbitrage opportunity. This works because in any two-outcome event, one of the outcomes must happen — meaning the true total probability is 100%, or 1. If the sum of the implied probabilities is less than 1, it means the market is undervaluing both outcomes, leaving a gap to exploit. By betting proportionally on both sides according to the odds, we can guarantee a profit regardless of which team wins. 
