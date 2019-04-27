import os
import pandas as pd
import numpy as np
import seaborn as sb
from python_pkg import python_udf as udf
import matplotlib.pyplot as plt
import random
import time


# =============================================================================
# Helper functions
# =============================================================================
def missing_data_percent(data):
    result = data.isna().sum() / data.shape[0]
    return result


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
    missing_data = missing_data_percent(data)
    #list all of the columns that have missing data
    missing_cols = list(missing_data[missing_data > threshold].sort_values(ascending=False).index)
    #drop the columns that have missing values above threshold
    result = data.drop(missing_cols, axis=1, inplace=False)
    
    return result


def simple_impute(data, threshold=0.25):
    """
    Simple impute using sklearn SimpleImputer class\n
    Numeric features use 'median'; Categorical features use 'most_frequent'
    """
    #import class
    from sklearn.impute import SimpleImputer
    
    #Build simple imputers for both numeric and categorical features
    numeric_impute = SimpleImputer(missing_values=np.NaN, strategy='median')
    cat_impute = SimpleImputer(missing_values=np.NaN, strategy='most_frequent')
    
    #missing data columns
    missing_data = missing_data_percent(data)
    
    #columns with missing values but less than or equal to 25%
    impute_cols = list(missing_data[(missing_data <= threshold) & (missing_data > 0)].sort_values(ascending=False).index)
    
    #create a dataframe of all of the features to impute
    missing_values_df = data.drop(data.columns.difference(impute_cols), axis=1, inplace=False)
    #numeric features to impute
    impute_numeric_col = missing_values_df.select_dtypes(include=np.number).columns
    #categorical features to impute
    impute_cat_col = missing_values_df.select_dtypes(exclude=np.number).columns
    
    #impute numerical features
    imputed_numeric_df = pd.DataFrame(numeric_impute.fit_transform(train_wr_miss.loc[:, impute_numeric_col]), columns=impute_numeric_col).add_prefix('imp_')
    


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


#impute the rest of the data




# =============================================================================
# Testing grounds
# =============================================================================
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline

test_pipeline = Pipeline([('remove_missing', FunctionTransformer(remove_missing_data)), ('impute', )])





























