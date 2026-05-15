import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss, mean_absolute_error, root_mean_squared_error
import seaborn as sns
import streamlit as st
import plotly.express as px

from sql.load_db_to_df import load_df_from_db
from data_science.data_science_functions import transform_shift_to_phase
from config import IMPORTANT_FEATURES

match_data_df = load_df_from_db('features', 'matches_eda')
match_data_df = transform_shift_to_phase(match_data_df[IMPORTANT_FEATURES])


for col in match_data_df.select_dtypes(exclude= 'number').columns.tolist():
    if col == 'actual_time':
        continue
    match_data_df[col] = match_data_df[col].astype('category')

match_data_df.sort_values(ascending = True, by = 'actual_time')

# X = match_data_df.drop(columns = 'total_score')

X = match_data_df[['team_key1','team_key2','team_key3','actual_time']]
Y = match_data_df['auto_points']

split_date = '2026-04-10'

X_train = X[X['actual_time'] < split_date].drop(columns ='actual_time')
y_train = Y[X['actual_time'] < split_date]
X_test = X[X['actual_time'] >= split_date].drop(columns ='actual_time')
y_test = Y[X['actual_time'] >= split_date]

model = lgb.LGBMRegressor(
    objective = 'regression',
    n_estimators = 1500,
    learning_rate = 0.05,
    num_leaves = 33,
    n_jobs = 1,
)

model.fit(X_train, y_train, eval_set = [(X_test, y_test)])

preds = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, preds):.2f}")
print(f"RMSE: {root_mean_squared_error(y_test, preds):.2f}")


st.plotly_chart(px.scatter(x = y_test, y = preds))



