import lightgbm as lgb
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import streamlit as st
import plotly.express as px

from sql.load_db_to_df import load_df_from_db

match_data_df = load_df_from_db('features', 'match_auto_data_calc')

slots_df = load_df_from_db('features', 'matches_eda')[
        ['match_key', 'team_key1', 'team_key2', 'team_key3', 'auto_points', 'actual_time', 'alliance']
]

slots_df = slots_df.drop_duplicates(subset=['match_key', 'alliance'])

stat_cols = [col for col in match_data_df.columns
             if col not in ['team_key', 'match_key', 'actual_time', 'auto_points', 'alliance', 'opp_auto_points']]

wide_df = slots_df.copy()
for i, team in enumerate(['team_key1', 'team_key2', 'team_key3'], 1):
    team_stats = (
        match_data_df[['team_key', 'match_key', 'alliance'] + stat_cols]
        .rename(columns={'team_key': team})
        .rename(columns={c: f't{i}_{c}' for c in stat_cols})
    )
    wide_df = wide_df.merge(team_stats, on=['match_key', team, 'alliance'], how='left')

print(wide_df.columns.tolist())
season_avgs = wide_df[[
    't1_mean_season_last_auto_points',
    't2_mean_season_last_auto_points',
    't3_mean_season_last_auto_points'
]].fillna(0).values
sort_order = np.argsort(season_avgs, axis=1)[:, ::-1]

for c in stat_cols:
    vals = wide_df[[f't1_{c}', f't2_{c}', f't3_{c}']].values
    wide_df[[f't1_{c}', f't2_{c}', f't3_{c}']] = vals[np.arange(len(vals))[:, None], sort_order]

feature_cols = [c for c in wide_df.columns if c.startswith(('t1_', 't2_', 't3_'))]
X = wide_df[feature_cols]
Y = wide_df['auto_points']

split_date = '2026-04-10'

train_mask = wide_df['actual_time'] < split_date
test_mask = wide_df['actual_time'] >= split_date

X_train = X[train_mask]
y_train = Y[train_mask]
X_test = X[test_mask]
y_test = Y[test_mask]

model = lgb.LGBMRegressor(
    objective='regression',
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=33,
    n_jobs=1,
)

model.fit(X_train, y_train, eval_set=[(X_test, y_test)])

preds = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, preds):.2f}")
print(f"RMSE: {root_mean_squared_error(y_test, preds):.2f}")

st.plotly_chart(px.scatter(x=y_test, y=preds))
