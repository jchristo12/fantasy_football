import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

#build the url
season = 2018
week = 1
full_url = 'https://fantasydata.com/nfl-stats/point-spreads-and-odds?season=' + str(season) + '&seasontype=1&week=' + str(week)

#scrape the data
page = requests.get(full_url)
#if page.status_code != 200:
#    sys.exit('There was a problem accessing the URL')
#else:
soup = BeautifulSoup(page.content, 'html.parser')
data = soup.find_all(name='div', attrs={'kendo-grid': 'grid'})


