import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lxml
import html5lib
from urllib.request import urlopen
import time

pd.set_option('display.max_columns',1000)
pd.set_option('display.max_rows',1000)


# Begin extracting historical odds data for games to compare our model's predictions and results against Vegas lines
# df1 = pd.read_html('https://www.oddsshark.com/stats/gamelog/baseball/mlb/27024?season=2022')[0] # [0]
