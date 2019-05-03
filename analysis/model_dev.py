#basic imports
import pandas as pd
import math
import numpy as np
import seaborn as sb
from python_pkg import python_udf as udf
import matplotlib.pyplot as plt
import random
import time
import importlib
#importlib.import_module('feature_analysis')

#sklearn imports
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import sklearn.metrics as metrics

#other imports
import xgboost as xgb


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

def missing_data_columns(data, threshold=0.25):
    """
    Store columns that have more than a threshold percent of total missing data
    """
    #find % of total rows with missing data
    missing_data = missing_data_percent(data)
    #list all of the columns that have missing data
    missing_cols = list(missing_data[missing_data > threshold].sort_values(ascending=False).index)
    #drop the columns that have missing values above threshold
    #result = data.drop(missing_cols, axis=1, inplace=False)
    
    return missing_cols

def remove_missing_data(data, threshold=0.25):
    """Drop the columns with too much missing data"""
    #cols with too much missing data
    cols = missing_data_columns(data, threshold=threshold)
    #drop the columns
    result = data.drop(cols, axis=1)
    
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

def perform_modeling(model_pipeline, param_grid, cv, score, train, y_train):
    """
    Perform a grid search on a estimator pipeline\n
        Return the fitted GridSearchCV object
    """
    #fit the GridSearch object
    grid = GridSearchCV(model_pipeline, param_grid, cv=cv, scoring=score, iid=False)
    #fit the model and perform CV
    fit_cv = grid.fit(train, y_train)
    #RMSE of best model
    rmse_cv = np.sqrt(fit_cv.best_score_)
    #Print model type
    print('Model type: %s' %model_pipeline.steps[len(model_pipeline.steps)-1][0])
    #Print best score
    print('Best score: %s' %rmse_cv)
    #Print best parameters
    print('Best parameters: %s' %fit_cv.best_params_)

    return fit_cv

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
#df = feature_analysis.main()
df = pd.read_csv('https://github.com/jchristo12/fantasy_football/blob/master/data/full_data.csv?raw=true')

#create home_away categorical variable
df['home_away'] = np.where(df['team']==df['h'], 'home', 'away')

#remove rows that have NaN for the shifted variables
df_clean = df[~df.loc[:,'seas_pa':'seas_tdret'].isna().all(axis=1)]

#store positions we are concerned about; will use these to filter out 
pos_of_interest = ['QB', 'RB', 'WR', 'TE']
#filter out positions we don't care about
df_clean2 = df_clean[df_clean['pos1'].isin(pos_of_interest)]

#set the column types
col_dtypes = {'category': ['seas', 'wk', 'pos1', 'team', 'udog', 'v', 'h', 'day', 'stad', 'wdir',
                          'surf', 'gen_cond', 'gen_dv', 'def_team', 'home_away']}
#flip the key and values around so they will work in the argument for 'astype()'
col_dtypes_alt = {old: new for new, old_all in col_dtypes.items() for old in old_all}
#make the change to column type
df_clean2 = df_clean2.astype(col_dtypes_alt)

#remove stat columns that we won't know at time of analysis
drop_stat_cols = list(df_clean2.loc[:, 'pa':'tdret'].columns)
#addl columns to drop
id_drop_cols = list(df_clean2.loc[:, 'pk':'full_name'])
addl_drop_cols = ['dob', 'udog', 'nflid', 'surf', 'ptsv', 'ptsh', 'h', 'v']
#combine all columns to drop
manual_drop_cols = drop_stat_cols + addl_drop_cols + id_drop_cols
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
#create a dataframe with all weeks of WR to do EDA
#only want to look at training data (the same training data that will be used later for model building)
all_train_df = []
for w in df_vet['wk'].unique():
    interim_df = divide_by_pos_wk(df_vet, 'WR', w)
    trn_df = train_test_split(interim_df, train_size=0.8, test_size=0.2, shuffle=True, random_state=67)[0]
    all_train_df.append(trn_df)
#combine all of the training data sets together into one giant dataset
df_eda = pd.concat(all_train_df, axis=0)

#drop columns
df_eda1 = df_eda.drop(manual_drop_cols, axis=1)
#remove columns with too much missing data
df_eda2 = remove_missing_data(df_eda1)
eda_missing = missing_data_percent(df_eda1)
eda_missing[eda_missing>0]

#separate numeric and categorical variables
num_cols, cat_cols = col_type_split(df_eda1)
#store summary statistics of interest
summ_stats = ['count', 'min', 'max', 'median', 'mean', 'std']

#boxplot of gen_cond types and f_pts
sb.boxplot(x='gen_cond', y='f_pts', data=df_eda2)
df_eda2.groupby(by='gen_cond').agg({'f_pts': summ_stats})

#home_away and f_pts
sb.boxplot(x='home_away', y='f_pts', data=df_eda2, hue='udog_binary')
df_eda2.groupby(by=['home_away', 'udog_binary']).agg({'f_pts': summ_stats})

#correlation of numerical variables
corr_thres = udf.corr_to_df_summary(df_eda2, threshold=0).reset_index()
corr_thres[corr_thres['Var2']=='f_pts'].sort_values(by='Pearson R', ascending=False)

#recent_recy to f_pts
sb.scatterplot(x='recent_recy', y='f_pts', data=df_eda2)
df_eda2.loc[df_eda2['recent_recy']>700, ['full_name']]

#college conference and exp
sb.scatterplot(x='exp', y='f_pts', data=df_eda2)
sb.boxplot(x='gen_dv', y='f_pts', data=df_eda2)


# =============================================================================
# Setup Pipelines
# =============================================================================
#Store columns to drop due to too much missing data
miss_cols = missing_data_columns(train_wr, threshold=0.25)
all_drop_cols = manual_drop_cols + miss_cols

#Build simple imputers for both numeric and categorical features
numeric_impute = SimpleImputer(missing_values=np.NaN, strategy='median')
cat_impute = SimpleImputer(missing_values=np.NaN, strategy='constant', fill_value='missing')

#one hot encoder for categorical variables
cat_onehotencode = OneHotEncoder()

#build different pipelines for numeric and categorical data
numeric_pipe = Pipeline(steps=[('dtype', TypeSelector(True)),
                               ('impute', numeric_impute)])

#numeric pipeline with standardizer
numeric_pipe_std = Pipeline(steps=[('dtype', TypeSelector(True)),
                                    ('standardize', StandardScaler()),
                                    ('impute', numeric_impute)])

cat_pipe = Pipeline(steps=[('dtype', TypeSelector(False)),
                            ('impute', cat_impute),
                            ('onehotencode', cat_onehotencode)])

#prepare the response data
y_train = train_wr['f_pts']
y_test = test_wr['f_pts']

#make a scoring metric for GridSearchCV
mse = metrics.make_scorer(metrics.mean_squared_error)

#preprocessing pipeline
preprocess_pipe = Pipeline(steps=[('subset_data', ColumnSelector(columns=all_drop_cols)),
                                ('drop_resp',FunctionTransformer(func=exclude_response, validate=False)),
                                ('feature_work', FeatureUnion(transformer_list=[('numeric_data', numeric_pipe),
                                                                                ('categorical_data', cat_pipe)],))])

#preprocessing pipeline with Standardizer
preprocess_pipe_std = Pipeline(steps=[('subset_data', ColumnSelector(columns=all_drop_cols)),
                                        ('drop_resp',FunctionTransformer(func=exclude_response, validate=False)),
                                        ('feature_work', FeatureUnion(transformer_list=[('numeric_data', numeric_pipe_std),
                                                                                        ('categorical_data', cat_pipe)],))])


# =============================================================================
# Modeling
# =============================================================================
#Random Forest
#modeling pipeline
rf_pipe = Pipeline(steps=[('preprocess', preprocess_pipe),
                            ('rf', RandomForestRegressor(n_estimators=50))])

#build the parameter grid to be used in GridSearch class
rf_param_grid = {'rf__max_depth': [3,5,7,10,15]}

#set the random number seed
random.seed(212)
#CV of random forest model using GridSearchCV
rf_model = perform_modeling(rf_pipe, rf_param_grid, cv=10, score=mse, train=train_wr, y_train=y_train)
#RMSE of best RF model
rf_rmse_cv = np.sqrt(rf_model.best_score_)



#XGBoost
#modeling pipeline
xgb_pipe = Pipeline(steps=[('preprocess', preprocess_pipe),
                            ('xgb', xgb.XGBRegressor(seed=212))])

#xgb parameter grid
xgb_param_grid = {'xgb__max_depth': [2, 3, 5, 6],
                    'xgb__eta': [0.1, 0.3, 0.5, 0.9]}

#Cross validation for XGB model
xgb_model = perform_modeling(xgb_pipe, xgb_param_grid, cv=10, score=mse, train=train_wr, y_train=y_train)
#Store mean CV RMSE score
xgb_rmse_cv = np.sqrt(xgb_model.best_score_)

#static parameter fitting
xgb_model = rf_pipe.fit(train_wr, y_train)
xgb_y_pred = xgb_model.predict(test_wr)
xgb_rmse = np.sqrt(metrics.mean_squared_error(y_test, xgb_y_pred))


#SVR
#modeling pipeline
svr_pipe = Pipeline(steps=[('preprocess', preprocess_pipe_std),
                            ('svr', SVR(kernel='rbf', C=1.0, epsilon=0.1))])

#SVR parameter grid
svr_param_grid = {'svr__C': [1.0],
                    'svr__epsilon': [0.1]}

#cross validation for svr
svr_model = perform_modeling(svr)



# =============================================================================
# Testing Grounds
# =============================================================================
pd.Series(rf_pipe.named_steps['rf'].feature_importances_).sort_values(ascending=False)

#test RemoveMissingData
testing = train_wr.copy()
victim = test_wr.copy()
victim.loc[(victim['wdir']=='CALM') | (victim['wdir']=='W'), 'wdir'] = np.NaN

miss_test = missing_data_percent(testing)
miss_test[miss_test>0]

miss_victim = missing_data_percent(victim)
miss_victim[miss_victim>0]


remove = RemoveMissingData(threshold=0.25)
remove_model = remove.fit(testing)

result = remove_model.transform(testing)
'wdir' in list(result.columns)

test_pipe = Pipeline(steps=[('remove_miss', RemoveMissingData(threshold=0.25))])

result2 = test_pipe.fit(testing)

#test inserting steps to pipeline
numeric_pipe.steps.insert(1, ['standardize', StandardScaler()])
numeric_pipe.steps[len(numeric_pipe.steps)-1][0]