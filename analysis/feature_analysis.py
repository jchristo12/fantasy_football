def main():
    #import basic packages
    try:
        import pandas as pd
        import numpy as np
        import math
        from python_pkg import python_udf as UDF
    except:
        print('Necessary packages not installed. Please install:')
        print('numpy, pandas, math, and python_pkg (UDF)')


    # =============================================================================
    # Help functions
    # =============================================================================
    def ratio_stat(num_col, denom_col, new_col, data):
        #import necessary packages to run the function
        try:
            import numpy as np
            import pandas as pd
        except:
            print('Necessary packages not installed. Please install:')
            print('numpy & pandas')
            
        #last game stat calc
        last_col_calc = data['last_' + num_col] / data['last_' + denom_col]
        last_col = last_col_calc.replace([np.inf, np.NaN], [data['last_' + num_col], 0])#.reset_index(drop=True)
        
        #career stat calc
        career_col_calc = data['career_' + num_col] / data['career_' + denom_col]
        career_col = career_col_calc.replace([np.inf, np.NaN], [data['career_' + num_col], 0])#.reset_index(drop=True)
        
        #season stat calc
        seas_col_calc = data['seas_' + num_col] / data['seas_' + denom_col]
        seas_col = seas_col_calc.replace([np.inf, np.NaN], [data['seas_' + num_col], 0])#.reset_index(drop=True)
        
        #rolling game stat calc
        rolling_col_calc = data['recent_' + num_col] / data['recent_' + denom_col]
        rolling_col = rolling_col_calc.replace([np.inf, np.NaN], [data['recent_' + num_col], 0])#.reset_index(drop=True)    
        
        #concate the series together
        added_df = pd.concat([data, career_col, seas_col, rolling_col, last_col], axis=1)
        added_df.rename(columns={0: 'career_'+new_col,
                                1: 'seas_'+new_col,
                                2: 'recent_'+new_col,
                                3: 'last_'+new_col}, inplace=True)


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


    #Add Age Feature
    #strip out the year from DOB
    dob_year = player_rolling_sort['dob'].apply(lambda x: int(str(x[-4:])))
    #add age to dataframe
    player_rolling_sort['age'] = player_rolling_sort['seas'].astype(int) - dob_year


    #College Conference combination
    #store the new categories
    power_five = ['Big 12', 'Big Ten', 'Atlantic Coast (ACC)', 'Southeastern (SEC)', 'Pacific 12']
    #if conference is in the power 5, then leave it. Otherwise, call it 'Other'
    player['gen_dv'] = pd.Series(np.where(player['dv'].isin(power_five), player['dv'], 'Other'), dtype='category')


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


    # =============================================================================
    # Final Prep for Model Dev
    # =============================================================================
    #list of columns that have been replaced by a transformation
    columns_to_drop = ['cond', 'dv']
    #drop columns and store as the final data frame
    model_df = full_df.drop(columns_to_drop, axis=1, inplace=False)

    return model_df


if __name__ == '__main__':
    main()