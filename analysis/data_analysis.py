import os
import pandas as pd
import numpy as np

#load the data
offense = pd.read_csv('C:/Users/Joe/Projects/fantasy_football/analysis/offense_final.csv', index_col='pk')
defense = pd.read_csv('C:/Users/Joe/Projects/fantasy_football/analysis/defense_final.csv', index_col='pk')
kicker = pd.read_csv('C:/Users/Joe/Projects/fantasy_football/analysis/kicker_final.csv', index_col='pk')