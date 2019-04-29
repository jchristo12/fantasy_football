import pandas as pd
import numpy as np
import seaborn as sb
from python_pkg import python_udf as udf
import matplotlib.pyplot as plt
import random
import time

#sklearn imports
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as metrics

# =============================================================================
# Helper functions
# =============================================================================
def missing_data_percent(data):
    """Calculate the percentage of total observations that are missing and return a pd.Series"""
    result = data.isna().sum() / data.shape[0]
    return result

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

def exclude_response(data, response_feat='f_pts'):
    """Drop the specified response feature from the data"""
    x_df = data.drop(response_feat, axis=1)
    return x_df

def col_type_split(data, col_type=np.number):
    """
    Return the column names for the specified data type and column names for the remaining features
    """
    num_cols = list(data.select_dtypes(include=col_type).columns)
    cat_cols = list(data.select_dtypes(exclude=col_type).columns)
    #return two lists: numeric and non-numeric columns
    return num_cols, cat_cols


# =============================================================================
# Transformer Classes
# =============================================================================
class ColumnSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to return a subset of a DataFrame\n
    Columns entered are the columns to drop
    """
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        #check if the object is a pandas dataframe
        assert isinstance(X, pd.DataFrame)
        #error handling
        try:
            #return the subset of the dataframe
            return X.drop(self.columns, axis=1)
        except KeyError:
            #return an error message if the specified columns aren't in the datframe
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError('The DataFrame does not include the columns: %s' %cols_error)

class TypeSelector(BaseEstimator, TransformerMixin):
    """
    Separates out the columns by data type. Mimics the 'ColumnTransformer' class\n
    'numeric' is a boolean value
    """
    def __init__(self, numeric):
        assert isinstance(numeric, bool)
        self.numeric = numeric

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        #set up for numeric columns and everything else
        if self.numeric == True:
            return X.select_dtypes(include=np.number)
        else:
            return X.select_dtypes(exclude=np.number)

class RemoveMissingData(BaseEstimator, TransformerMixin):
    """Remove features where the percentage of rows with missing data is above a threshold"""
    def __init__(self, threshold=0.25):
        self.threshold = threshold

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        output = remove_missing_data(data=X, threshold=self.threshold)
        return output


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

#remove stat columns that we won't know at time of analysis
drop_stat_cols = list(df_clean2.loc[:, 'pa':'tdret'].columns)
#addl columns to drop
more_drop_cols = list(df_clean2.loc[:, 'pk':'full_name'])
addl_drop_cols = ['dob', 'udog', 'nflid']
#combine all columns to drop
all_drop_cols = drop_stat_cols + addl_drop_cols + more_drop_cols
#find the columns to use in analysis
#cols_to_use = list(set(list(df_clean2.columns)).difference(all_drop_cols))


#store dataframe of non-rookies
df_vet = df_clean2.loc[df_clean2['exp']!=1, :]
#store dataframe of rookie data
df_rook = df_clean2.loc[df_clean2['exp']==1, :]

#segment out for WR and week 10
df_wr10 = divide_by_pos_wk(df_vet, 'WR', 10)

#break out the data between training and test
train_wr, test_wr = train_test_split(df_wr10, train_size=0.8, test_size=0.2, shuffle=True, random_state=67)
#reset index on both dataframes
train_wr = train_wr.reset_index(drop=True)
test_wr = test_wr.reset_index(drop=True)


# =============================================================================
# EDA
# =============================================================================
#drop columns
df_eda1 = train_wr.drop(all_drop_cols, axis=1)

#separate numeric and categorical variables
num_cols, cat_cols = col_type_split(df_eda1)

#remove columns with too much missing data
df_eda2 = remove_missing_data(df_eda1)
eda_missing = missing_data_percent(df_eda1)
eda_missing[eda_missing>0]


# =============================================================================
# Setup Pipelines
# =============================================================================
#impute the rest of the data    
#Build simple imputers for both numeric and categorical features
numeric_impute = SimpleImputer(missing_values=np.NaN, strategy='median')
cat_impute = SimpleImputer(missing_values=np.NaN, strategy='constant', fill_value='missing')

#one hot encoder for categorical variables
cat_onehotencode = OneHotEncoder()

#build different pipelines for numeric and categorical data
numeric_pipe = Pipeline(steps=[('dtype', TypeSelector(True)),
                               ('impute', numeric_impute)])

cat_pipe = Pipeline(steps=[('dtype', TypeSelector(False)),
                            ('impute', cat_impute),
                            ('onehotencode', cat_onehotencode)])

#prepare the response data
y_train = train_wr['f_pts']
y_test = test_wr['f_pts']

#make a scoring metric for GridSearchCV
mse = metrics.make_scorer(metrics.mean_squared_error)


# =============================================================================
# Modeling
# =============================================================================
#preprocessing pipeline
preprocess_pipe = Pipeline(steps=[('subset_data', ColumnSelector(columns=all_drop_cols)),
                                ('drop_resp',FunctionTransformer(func=exclude_response, validate=False)),
                                ('remove_missing', RemoveMissingData(threshold=0.25)),
                                ('feature_work', FeatureUnion(transformer_list=[('numeric_data', numeric_pipe),
                                                                                ('categorical_data', cat_pipe)],))])
#modeling pipeline
rf_pipe = Pipeline(steps=[('preprocess', preprocess_pipe),
                             ('rf', RandomForestRegressor(n_estimators=50))])

#build the parameter grid to be used in GridSearch class
rf_param_grid = {'rf__max_depth': [5, 10]}

#create the GridSearch class
rf_grid = GridSearchCV(rf_pipe, rf_param_grid, cv=10, scoring=mse, iid=False)
#Fit the model using CV
rf_grid.fit(train_wr, y_train)
#RMSE of best model
rf_rmse = np.sqrt(rf_grid.best_score_)


# =============================================================================
# Testing Grounds
# =============================================================================
pd.Series(rf_pipe.named_steps['rf'].feature_importances_).sort_values(ascending=False)