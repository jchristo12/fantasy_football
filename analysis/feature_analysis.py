def prep_for_modeling():
#import basic packages
try:
    import pandas as pd
    import numpy as np
    import math
    from python_pkg import python_udf as udf
except:
    print('Necessary packages not installed. Please install:')
    print('numpy, pandas, math, and python_pkg (UDF)')


# =============================================================================
# Help functions
# =============================================================================
def replace_ratio_values(calc, prefix, data, num_col):
    """Helper function to be used in the 'ratio_stat' function"""
    #create the map of value to replace and with what
    #replace_dict = {np.inf: data[prefix + num_col],
    #                -np.inf: data[prefix + num_col],
    #                np.NaN: 0}

    #alternate method to replace - lists
    to_replace = [np.inf, -np.inf, np.NaN]
    values = [data[prefix + num_col], data[prefix + num_col], 0]
    
    #perform the replacement using the replacement dictionary
    col_result = calc.replace(to_replace=to_replace, value=values)
    return col_result

def ratio_stat(num_col, denom_col, new_col, data):
    """Calculate the ratio statistic for all of the statistic versions (i.e. rolling, last, career, seas)"""
    #import necessary packages to run the function
    try:
        import numpy as np
        import pandas as pd
    except:
        print('Necessary packages not installed. Please install:')
        print('numpy & pandas')

    #last game stat calc
    last_col_calc = data['last_' + num_col] / data['last_' + denom_col]
    last_col = replace_ratio_values(last_col_calc, 'last_', data=data, num_col=num_col)
    
    #career stat calc
    career_col_calc = data['career_' + num_col] / data['career_' + denom_col]
    career_col = replace_ratio_values(career_col_calc, 'career_', data=data, num_col=num_col)
    
    #season stat calc
    seas_col_calc = data['seas_' + num_col] / data['seas_' + denom_col]
    seas_col = replace_ratio_values(seas_col_calc, 'seas_', data=data, num_col=num_col)
    
    #rolling game stat calc
    rolling_col_calc = data['recent_' + num_col] / data['recent_' + denom_col]
    rolling_col = replace_ratio_values(rolling_col_calc, 'recent_', data=data, num_col=num_col)
    
    #concate the series together
    added_df = pd.concat([data, career_col, seas_col, rolling_col, last_col], axis=1)
    added_df.rename(columns={0: 'career_'+new_col,
                            1: 'seas_'+new_col,
                            2: 'recent_'+new_col,
                            3: 'last_'+new_col}, inplace=True)

    return added_df

def add_depth_chart_rank(data, pos_grid, ranks):
    """
    Add the rankings to the orig dataframe. 
        Returns the orig data frame with added rank column
    """
    #create the feature in the dataframe
    data['pos_rank'] = np.NaN
    #initialize the indexer
    x = 0
    
    #loop through all of the calculated ranks (by pos) and add to dataframe
    for d in ranks:
        keys = list(pos_grid.keys())
        data.loc[data['pos1']==keys[x], 'pos_rank'] = d.values
        x += 1
    
    #convert ranks to categoricals
    data = data.astype({'pos_rank': 'category'})
        
    return data

def depth_chart(data, pos_grid, asc=False, add_to_df=False):
    """
    Calculate depth chart positions for each player by week, team, seas, and position\n
        Option to return the original dataframe with added pos_rank feature or a list of rank df's
    """
    #make sure asc argument is boolean
    assert isinstance(asc, bool)
    #make sure pos_grid is a dictionary
    assert isinstance(pos_grid, dict)
    #make sure add_to_df is boolean
    assert isinstance(add_to_df, bool)
    
    #store the positions
    keys = list(pos_grid.keys())
    #initialize list for all ranked dataframes
    results = []
    
    for p in keys:
        #subset data
        df = data[data['pos1']==p]
        #group the data by team, seas, and wk
        grouped = df.groupby(by=['team', 'seas', 'wk'], as_index=False, sort=False)
        #rank based on specified stat
        ranked = grouped[pos_grid[p]].rank(method='min', ascending=asc)
        ranked.columns = [p+'_rank']
        
        #add data frame to list
        results.append(ranked)
    
    #if true, returns the original df with added pos rank column
    #if false, returns the list of data frames with ranks for each pos
    if add_to_df == False:
        return results
    else:
        output_df = add_depth_chart_rank(data, pos_grid, results)
        return output_df

def summ_by_team(data, team_col):
    """Aggregate stats per player by team\n
        Returns a dataframe"""
    #group the data by season and wk and only return the orig stats
    tsw = data.groupby(by=[team_col, 'seas', 'wk'], as_index=True).sum().loc[:, 'pa':'tdret']
    #data.groupby(by=[team_col, 'seas', 'wk'], as_index=True).sum()[orig_stats]
    
    #remove the bye weeks
    tsw_no_bye = tsw[tsw.notna().all(axis=1)].reset_index([team_col, 'seas', 'wk'])
    
    return tsw_no_bye

def rolling_team_stats(data, team_col, window=4):
    """Calculate the rolling aggregation of the team states by season\n
        Returns a data frame"""
    #store the identifiying feature
    identifiers = data.loc[:, [team_col, 'seas', 'wk']]
    
    #lag by one week
    tsw_lagged = data.groupby(by=[team_col, 'seas']).shift(1).drop('wk', axis=1)
    #re-add identifiers
    tsw_full = pd.concat([identifiers, tsw_lagged], axis=1)
    
    #remove the NaN weeks (due to lag)
    tsw_clean = tsw_full[tsw_full.loc[:, 'pa':'tdret'].notna().all(axis=1)]
    #tsw_clean = tsw_full[tsw_full[orig_stats].notna().all(axis=1)]
    #store the identifying features again
    clean_identifiers = tsw_clean.loc[:, [team_col, 'seas', 'wk']]
    
    #calculate the rolling agg
    summ = tsw_clean.groupby(by=[team_col, 'seas'], sort=False).rolling(window=window, min_periods=1).sum().reset_index().loc[:, 'fuml':'trg']
    #summ = tsw_clean.groupby(by=[team_col, 'seas'], sort=False).rolling(window=window, min_periods=1).sum().reset_index()[orig_stats]
    
    #add the identifiers
    summ_clean = pd.concat([clean_identifiers.reset_index(drop=True), summ.reset_index(drop=True)], axis=1)
    
    return summ_clean

def team_rank(data, stat_col, asc=True):
    """Calculate each team's rank for a given week for a given stat column\n
        Returns a nx1 data frame of the rankings"""
    #assert that asc is boolean
    assert isinstance(asc, bool)
    
    #group and perform the ranking
    group = data.groupby(by=['seas', 'wk'], as_index=False, sort=False)
    rank = group[stat_col].rank(method='min', ascending=asc)
    #add a suffix to the data
    rank.columns = [stat_col + '_rank']
    
    return rank

def combo_team_rank(data, team_col, stat_col, window=4):
    """Combine all of the ranking functions\n
        Returns a dataframe"""
    df1 = summ_by_team(data, team_col)
    df2 = rolling_team_stats(df1, team_col, window=window)
    result = team_rank(df2, stat_col)
    return result


# =============================================================================
# Read in the data
# =============================================================================
#player data
player = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/predictor/player_offense.csv')

#game data
game = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/predictor/game.csv')

#response variable
response = pd.read_csv('https://raw.githubusercontent.com/jchristo12/fantasy_football/master/data/response/offense_final.csv', header=0, usecols=['pk', 'f_pts'])


# =============================================================================
# Clean up the data
# =============================================================================
#rename columns
player.rename(columns={'seas.1': 'exp'}, inplace=True)

#convert column types
#player data
player = player.astype({'seas': 'category',
        'wk': 'category',
        'team': 'category',
        'pos1': 'category',
        'dv': 'category',
        'exp': 'category'})
#game data
game = game.astype({'v': 'category',
                'h': 'category',
                'day': 'category',
                'cond': 'category',
                'stad': 'category',
                'wdir': 'category',
                'surf': 'category'})

#replace Pacific 10 with Pacific 12 (name change)
player['dv'].replace('Pacific 10', 'Pacific 12', inplace=True)

#Replace zeros with NaN where appropriate
#store all of the combine columns
combine_cols = list(player.loc[:, 'forty':'hand'].columns)
#replace combine stats that are zero with NaN
player[combine_cols] = player[combine_cols].replace(0, np.NaN)

#replace height and weight that are zeros with NaN
player[['height', 'weight']] = player[['height', 'weight']].replace(0, np.NaN)


# =============================================================================
# Player Feature Creation
# =============================================================================
#Player Data

#lagged stats
#sort the stats
player_sorted = player.sort_values(by=['player', 'gid'], ascending=True)

#last game stats
last_stats = player_sorted.groupby(by=['player', 'seas']).shift(1).loc[:, 'pa':'tdret'].add_prefix('last_')

#group stats
#group, lag, and calculate the cumulative sum of all of the stats
career_stats = pd.concat([player_sorted['player'], player_sorted.groupby(by='player', group_keys=True).shift(1).loc[:, 'pa':'tdret']], axis=1).groupby('player').cumsum().loc[:, 'pa':'tdret'].add_prefix('career_')

#rolling stats
#group by player and season and then lag the data by 1 week
lagged_stats = player_sorted.groupby(by=['player', 'seas']).shift(1).loc[:, 'pa':'tdret']
#Combine the player and season variables to the lagged data as identifers
lagged_id = pd.concat([player_sorted.loc[:, ['player', 'seas']], lagged_stats], axis=1)
#group by the player and season again and compute the 4 game rolling sum
recent_multi = lagged_id.groupby(by=['player', 'seas'], as_index=True).rolling(window=4, min_periods=1).sum().add_prefix('recent_')
#fix the index on the lagged, rolling stats
recent_stats = recent_multi.reset_index(level=[0,1], drop=True)

#season stats
lagged_stats = player_sorted.groupby(by=['player', 'seas']).shift(1).loc[:, 'pa':'tdret']
lagged_id = pd.concat([player_sorted.loc[:, ['player', 'seas']], lagged_stats], axis=1)
seas_stats = lagged_id.groupby(by=['player', 'seas'], as_index=False).cumsum().add_prefix('seas_')

#add all of the lagged stats together
player_rolling_sort = pd.concat([player_sorted, last_stats, recent_stats, seas_stats, career_stats], axis=1)


#Ratio Stat features
#Passing
#Passing completion
player_rolling_sort = ratio_stat('pc', 'pa', 'comp_pct', data=player_rolling_sort)
#touchdown to interception
player_rolling_sort = ratio_stat('tdp', 'ints', 'td_to_int', data=player_rolling_sort)
#Passing yards per completion
player_rolling_sort = ratio_stat('py', 'pc', 'yds_per_comp', data=player_rolling_sort)

#Rushing
#Yards per rush
player_rolling_sort = ratio_stat('ry', 'ra', 'ryds_per_carry', data=player_rolling_sort)
#Carries to touchdown ratio
player_rolling_sort = ratio_stat('ra', 'tdr', 'carry_to_td', data=player_rolling_sort)
#Carries to fumbles lost ratio
player_rolling_sort = ratio_stat('ra', 'fuml', 'carry_to_fuml', data=player_rolling_sort)

#Receiving
#catch percent (catches/targets)
player_rolling_sort = ratio_stat('rec', 'trg', 'catch_pct', data=player_rolling_sort)
#yards per catch
player_rolling_sort = ratio_stat('recy', 'rec', 'yds_per_rec', data=player_rolling_sort)
#rec to td's
player_rolling_sort = ratio_stat('rec', 'tdrec', 'rec_to_td', data=player_rolling_sort)

#Return
#average return yards
player_rolling_sort = ratio_stat('rety', 'ret', 'avg_ret', data=player_rolling_sort)
#returns to td's
player_rolling_sort = ratio_stat('ret', 'tdret', 'ret_to_td', data=player_rolling_sort)


#Depth Chart (based on rolling 4 game stats)
#create grid
depth_chart_grid = {'QB': 'recent_pa',
                    'RB': 'recent_ra',
                    'WR': 'recent_trg',
                    'TE': 'recent_trg'}

player_rolling_sort = depth_chart(player_rolling_sort, depth_chart_grid, asc=False, add_to_df=True)



#Add Age Feature
#strip out the year from DOB
dob_year = player_rolling_sort['dob'].apply(lambda x: int(str(x[-4:])))
#add age to dataframe
player_rolling_sort['age'] = player_rolling_sort['seas'].astype(int) - dob_year


#College Conference combination
#store the new categories
power_five = ['Big 12', 'Big Ten', 'Atlantic Coast (ACC)', 'Southeastern (SEC)', 'Pacific 12']
#if conference is in the power 5, then leave it. Otherwise, call it 'Other'
player_rolling_sort['gen_dv'] = pd.Series(np.where(player_rolling_sort['dv'].isin(power_five), player_rolling_sort['dv'], 'Other'), dtype='category')


# =============================================================================
# Game Feature Creation
# =============================================================================
#add underdog category
game['udog'] = pd.Series(np.where(game['sprv'] > 0, game['v'], game['h']), dtype='category')

#Game Conditions
#dictionary of general conditions
general_cond = {'indoor_cond': ['Closed Roof', 'Covered Roof', 'Dome'], 
                'percip_cond': ['Flurries', 'Light Rain', 'Light Showers', 'Light Snow',
                                'Rain', 'Showers', 'Snow', 'Thunderstorms', 'Chance Rain'],
                'fair_cond': ['Clear', 'Sunny', 'Cloudy', 'Cold', 'Fair', 'Foggy', 'Hazy', 'Mostly Cloudy',
                            'Mostly Sunny', 'Overcast', 'Partly Cloudy', 'Partly CLoudy', 'Partly Sunny',
                            'Sunny', 'Windy']}
#map the keys to each value to be used in category creation
general_cond_flipped = udf.dict_key_value_flip(general_cond)
#create a general conditions feature
game['gen_cond'] = game['cond'].apply(lambda x: general_cond_flipped[x])

#Fix Indoor 'wdir' and 'humd'
#for all indoor cond, set the wdir and humd to what makes sense for indoor playing conditions
game.loc[game['gen_cond']=='indoor_cond', ['wdir', 'humd']] = ['CALM', 45]


# =============================================================================
# Merge Data
# =============================================================================
#player data to game data
player_game = player_rolling_sort.merge(game, how='left', on='gid', suffixes=('_poff', '_game'))
#player+game data to response data
full_df = player_game.merge(response, on='pk', how='left')

#add variables that require merged data
full_df['udog_binary'] = full_df['team'].eq(full_df['udog'])


#Defensive Team feature
#create a new categorical column of the defensive team
full_df['def_team'] = pd.Series(np.where(full_df['team'] == full_df['h'], full_df['v'],
                                            full_df['h']), dtype='category')


#Defensive Team Rankings
def_team_agg = summ_by_team(full_df, 'def_team')
def_team_roll = rolling_team_stats(def_team_agg, 'def_team', window=4)

#separate stats based on if it is better to be low or high
stats_asc = list(set(list(full_df.loc[:, 'pa':'tdret'].columns)) - set(['ints', 'fuml']))
stats_desc = ['ints', 'fuml']
#loop thru each stat col and get the ranking
#initialize a list
def_ranks = []
#ascending ranks
for dc in stats_asc:
    output = team_rank(def_team_roll, dc, asc=True)
    def_ranks.append(output)
#descending ranks
for dc in stats_desc:
    output = team_rank(def_team_roll, dc, asc=False)
    def_ranks.append(output)
#combine all rankings into 1 dataframe
all_def_ranks = pd.concat(def_ranks, axis=1)


#Offensive Team Rankings
off_team_agg = summ_by_team(full_df, 'team')
off_team_roll = rolling_team_stats(off_team_agg, 'team', window=4)

#loop through
#initialize the list
off_ranks = []
#ascending ranks
for oc in stats_desc:
    output = team_rank(off_team_roll, oc, asc=True)
    off_ranks.append(output)
#descending ranks
for oc in stats_asc:
    output = team_rank(off_team_roll, oc, asc=False)
    off_ranks.append(output)
#combine all rankings into 1 dataframe
all_off_ranks = pd.concat(off_ranks, axis=1)


# =============================================================================
# Final Prep for Model Dev
# =============================================================================
#list of columns that have been replaced by a transformation
columns_to_drop = ['cond', 'dv']
#drop columns and store as the final data frame
model_df = full_df.drop(columns_to_drop, axis=1, inplace=False)

return model_df


if __name__ == '__main__':
    prep_for_modeling()
