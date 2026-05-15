import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, mean_absolute_error, root_mean_squared_error
from sklearn.linear_model import Lasso
from scipy.optimize import nnls
import streamlit as st
import plotly.express as px


from sql.load_db_to_df import load_df_from_db
from data_science.data_science_functions import transform_shift_to_phase
from config import IMPORTANT_FEATURES


split_date = '2026-04-10'
key_column = 'phase1_points'

match_data_df = load_df_from_db('features', 'matches_eda')
match_data_df = transform_shift_to_phase(match_data_df[IMPORTANT_FEATURES])
match_data_df.sort_values(ascending = True, by = 'actual_time', inplace= True)
match_data_df = match_data_df[['team_key1','team_key2','team_key3', key_column, 'actual_time']]

match_data_df_test = match_data_df[match_data_df['actual_time'] >= split_date].drop(columns = 'actual_time').reset_index()
match_data_df_train = match_data_df[match_data_df['actual_time'] < split_date].drop(columns = 'actual_time').reset_index()

teams = sorted(set(match_data_df_train[['team_key1','team_key2','team_key3']].values.ravel()))
team_idx = {t:i for i,t in enumerate(teams)}

X = np.zeros((len(match_data_df_train),len(teams)))

for i,row in match_data_df_train.iterrows():
    for t in [row.team_key1, row.team_key2, row.team_key3]:
        X[i,team_idx[t]] = 1

y = match_data_df_train[key_column].values

beta, *_ = np.linalg.lstsq(X, y, rcond = None)

opr = dict(zip(teams,beta))

y_pred = []
y_test = []
y_test_df = match_data_df_test.drop(columns = ['team_key1','team_key2','team_key3']).reset_index(drop = True)
team_test = match_data_df_test[['team_key1','team_key2','team_key3']].reset_index(drop = True)
for row in range(len(team_test)):
    pred = 0
    for team in team_test.loc[row]:
        if team not in teams:
            continue
        pred += opr[team]
    y_pred.append(pred)
    y_test.append(int(y_test_df.loc[row][key_column]))


print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"RMSE: {root_mean_squared_error(y_test, y_pred):.2f}")


st.plotly_chart(px.scatter(x = y_test, y = y_pred))

X = match_data_df[['team_key1','team_key2','team_key3','actual_time']]
Y = match_data_df[key_column]

X_train = X[X['actual_time'] < split_date].drop(columns ='actual_time')
y_train = Y[X['actual_time'] < split_date]
X_test = X[X['actual_time'] >= split_date].drop(columns ='actual_time')
y_test = Y[X['actual_time'] >= split_date]
# X_train_encoded = 

model = Lasso(positive=True, alpha = 0.5, fit_intercept = False)
model.fit(X_train,y_test)

preds = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, preds):.2f}")
print(f"RMSE: {root_mean_squared_error(y_test, preds):.2f}")

st.plotly_chart(px.scatter(x = y_test, y = preds))
