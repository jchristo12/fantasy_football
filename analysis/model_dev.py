import os
import pandas as pd
import numpy as np
import seaborn as sb
from python_pkg import python_udf as udf
import matplotlib.pyplot as plt
import random
import time


# =============================================================================
# Functions
# =============================================================================
def divide_by_pos_wk(data, pos, wk):
    """
    Take a dataframe, position, and week and return the subset of the data in a new dataframe.
    """
    df = data[(data['pos1']==pos) & (data['wk']==wk)]
    return df
    
def remove_missing_data(data, threshold=0.25):
    """
    Remove data that has more than the threshold % of missing values
    """
    #find % of total rows with missing data
    missing_data_pct = data.isna().sum() / data.shape[0]
    #list all of the columns that have missing data
    missing_cols = list(missing_data_pct[missing_data_pct > threshold].sort_values(ascending=False).index)
    #drop the columns that have missing values above threshold
    result = data.drop(missing_cols, axis=1, inplace=False)
    
    return result
    

# =============================================================================
# Data Setup
# =============================================================================
#import the data
df = pd.read_csv('https://github.com/jchristo12/fantasy_football/blob/master/data/full_data.csv?raw=true')

#remove rows that have NaN for the shifted variables
df_clean = df[~df.loc[:,'seas_pa':'seas_tdret'].isna().all(axis=1)]

#store positions we are concerned about; will use these to filter out 
pos_of_interest = ['QB', 'RB', 'WR', 'TE']
#filter out positions we don't care about
df_clean2 = df_clean[df_clean['pos1'].isin(pos_of_interest)]

#set the column types
col_dtypes = {'category': ['seas', 'wk', 'pos1', 'team', 'udog', 'v', 'h', 'day', 'stad', 'wdir',
                          'surf', 'gen_cond', 'gen_dv', 'def_team']}
#flip the key and values around so they will work in the argument for 'astype()'
col_dtypes_alt = {old: new for new, old_all in col_dtypes.items() for old in old_all}
#make the change to column type
df_clean2 = df_clean2.astype(col_dtypes_alt)

#store dataframe of non-rookies
df_vet = df_clean2.loc[df_clean2['exp']!=1, :]
#store dataframe of rookie data
df_rook = df_clean2.loc[df_clean2['exp']==1, :]

#segment out for WR and week 10
df_wr10 = divide_by_pos_wk(df_vet, 'WR', 10)


# =============================================================================
# Data Analysis
# =============================================================================
from sklearn.model_selection import train_test_split

#set the random seed for reproducability
random.seed(837)

#break out the data between training and test
train_wr, test_wr = train_test_split(df_wr10, train_size=0.75, test_size=0.25, shuffle=True)
#reset index on both dataframes
train_wr = train_wr.reset_index(drop=True)
test_wr = test_wr.reset_index(drop=True)

#remove columns with too much missing data
train_wr_miss = remove_missing_data(train_wr)
































