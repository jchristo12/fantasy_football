import os
import pandas as pd
import numpy as np

# =============================================================================
# Data initialization
# =============================================================================
#read in response data
r_offense = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_offense.csv')
r_defense = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_defense.csv')
r_kicker = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_kickers.csv')
r_sacks = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_sacks_on_qb.csv')

#convert data types in columns
#offense
r_offense = r_offense.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'player': str,
                          'pos1': 'category'})

#defense
r_defense = r_defense.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'team': 'category'})

#kicker
r_kicker = r_kicker.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'fkicker': str,
                          'good': 'category'})
#change column name of fkicker
r_kicker.rename(columns={'fkicker': 'player'}, inplace=True)

#sacks
r_sacks = r_sacks.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'qb': str})
#rename qb to player
r_sacks.rename(columns={'qb': 'player'}, inplace=True)

#combine offense and sacks (for QBs)
r_offense_test = r_offense.join(r_sacks, on='pk', how='left')