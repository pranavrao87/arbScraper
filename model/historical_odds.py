# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lxml
import html5lib
from urllib.request import urlopen
import time
import requests
from bs4 import BeautifulSoup
from pprint import pprint

pd.set_option('display.max_columns',1000)
pd.set_option('display.max_rows',1000)


URL = "https://www.oddsshark.com/stats/gamelog/baseball/mlb/27024?season=2021"
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
tables = soup.find_all('table')
