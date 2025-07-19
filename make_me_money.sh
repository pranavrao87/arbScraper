#!/bin/bash

echo "Running FanDuel scraper"
python3 arb_MLB_FD.py

echo "Running DraftKings scraper"
python3 arb_MLB_DK.py

echo "Running arbitrage calculator"
python3 arb_calc.py

echo "All scripts finished."
