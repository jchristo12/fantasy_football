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
r_offense.seas = r_offense.seas.astype('category')
r_offense.wk = r_offense.wk.astype('category')
r_offense.player = r_offense.player.astype('str')
r_offense.pos1 = r_offense.pos1.astype('category')

#defense
r_defense.seas = r_defense.seas.astype('category')
r_defense.wk = r_defense.wk.astype('category')
r_defense.team = r_defense.team.astype('category')

#kicker
r_kicker.seas = r_kicker.seas.astype('category')
r_kicker.wk = r_kicker.wk.astype('category')
r_kicker.fkicker = r_kicker.fkicker.astype('category')
r_kicker.good = r_kicker.good.astype('category')
#change column name of fkicker
r_kicker.rename(columns={'fkicker': 'player'}, inplace=True)

#sacks
r_sacks.seas = r_sacks.seas.astype('category')
r_sacks.wk = r_sacks.wk.astype('category')
r_sacks.qb = r_sacks.qb.astype('str')
#rename qb to player
r_sacks.rename(columns={'qb': 'player'}, inplace=True)
