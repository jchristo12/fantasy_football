import pandas as pd
#import numpy as np

# =============================================================================
# Helper funtions
# =============================================================================
#convert stat categories to fantasy points
def stats_to_pts(df, pts_dict, stat_col_start):
    """
    Converts the stats of a player to the appropriate fantasy point values\n
    Returns the original dataframe with a new column with the total fantasy points
    """
    #find the total columns with stats in it (add 1 for indexing)
    tot_stat_cols = len(df.columns[stat_col_start:]) + 1
    
    #loop through all columns with stats in them
    i = stat_col_start
    all_pts = []
    while i <= tot_stat_cols:
        col = df.columns[i]
        pts = df[col] * pts_dict[col]
        all_pts.append(pts)
        i += 1
    
    #merge all of the pts series together
    tot_pts = pd.concat(all_pts, axis=1)
    tot_pts = tot_pts.apply(sum, axis=1)
    #add fantasy points to the dataframe
    df['f_pts'] = tot_pts
    #return the original dataframe with the added fantasy points column
    return df


# =============================================================================
# Data initialization
# =============================================================================
#read in response data
r_offense = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_offense.csv')
r_defense = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_defense.csv')
r_kicker = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_kickers.csv')
r_sacks = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response_sacks_on_qb.csv')

#convert data types in columns and set pk as index
#offense
r_offense = r_offense.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'player': str,
                          'pos1': 'category'})
r_offense = r_offense.set_index('pk')
    
#defense
r_defense = r_defense.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'team': 'category'})
r_defense = r_defense.set_index('pk')
#parse out pts allowed column


#kicker
r_kicker = r_kicker.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'fkicker': str,
                          'good': 'category'})
r_kicker = r_kicker.set_index('pk')
#change column name of fkicker
r_kicker.rename(columns={'fkicker': 'player'}, inplace=True)

#sacks
r_sacks = r_sacks.astype({'pk': str,
                          'seas': 'category',
                          'wk': 'category',
                          'qb': str})
r_sacks = r_sacks.set_index('pk')
#rename qb to player
r_sacks.rename(columns={'qb': 'player'}, inplace=True)

#combine offense and sacks (for QBs)
r_offense = r_offense.join(r_sacks.tot_sack, how='left')
#fill NaNs with zeros (they are players that can't be sacked)
r_offense.tot_sack.fillna(0, inplace=True)

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
