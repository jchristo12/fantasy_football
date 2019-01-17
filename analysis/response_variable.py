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
#parse out pts allowed column


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
#r_offense_test = r_offense.join(r_sacks, on='pk', how='left')

# =============================================================================
# Convert data to fantasy pts
# =============================================================================
#offense
pts_off = {'py': 1/25, 'ints': -2, 'sack': -0.25, 'tdp': 4, 'ry': 1/10, 'tdr': 6, 'recy': 1/10, 'tdrec': 6, 'rety': 1/35,
               'tdret': 6, 'fuml': -2, 'conv': 2}
#defense
pts_def = {'sck': 1, 'saf': 4, 'blk': 3, 'ints': 2, 'frcv': 2, 'tdd': 6, 'tdret': 6, 'allow_0': 10, 'allow_1-6': 7,
           'allow_7-13': 4, 'allow_14-20': 1, 'allow_21-27': 0, 'allow_28-34': -1, 'allow_35+': -4}
#kicker
pts_kicker_g = {'0-19': 3, '20-29': 3, '30-39': 3, '40-49': 4, '50+': 5, 'XP': 1}
pts_kicker_m = {'0-19': -3, '20-29': -2, '30-39': -2, '40-49': -1, '50+': 0, 'XP': -2}