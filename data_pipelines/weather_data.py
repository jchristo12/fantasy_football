import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

#build the url
season = 2017
week = 16
base_url = 'http://www.nflweather.com/en/week/'
full_url = base_url + str(season) + '/week-' + str(week)

#scrape the data
page = requests.get(full_url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find_all('tbody')[0]

#used for testing
game = table.find_all('tr')[0]
#for each game, pull the teams, weather, and wind info
for game in table.find_all('tr'):
    #data to parse
    data = game.find_all('td', {'class': 'text-center'})
    #find the teams
    away = data[0].find('a').get_text()
    home = data[1].find('a').get_text()
    
    #find the weather forecast and trip the whitespace
    weather = data[5].get_text().strip()
    #parse out the temp and conditions; error handling for domes (i.e. no temps)
    try:
        temp = int(weather[:weather.find('f')])
    except:
        temp = np.NaN
    cond = weather[weather.find(' ') + 1:].strip()
    
    #find the wind info
    wind = data[6].get_text().strip()
    #parse out the speed and direction
    try:
        speed = int(wind[:wind.find('m')])
    except:
        speed = np.NaN
    direction = wind[wind.find(' '):].strip()
    
    print(away, home, str(temp), cond, str(speed), direction)