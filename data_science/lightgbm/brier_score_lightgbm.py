from sklearn.metrics import root_mean_squared_error, brier_score_loss
import pandas as pd
import numpy as np
import joblib
from sklearn.utils import resample
import lightgbm as lgb
from scipy.stats import norm
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


from sql.load_db_to_df import load_df_from_db
from config import  auto_point_reg_gbm
from data_science.pipeline.split_train_test_data import split_train_test_data_from_target_column_feature_columns_and_date



#import best parameters from optuna study and sql data
match_auto_data_df = load_df_from_db(schema = 'features', table = 'match_auto_data_calc')
match_auto_data_df['auto_won'] = (match_auto_data_df['auto_points'] > match_auto_data_df['opp_auto_points']).astype(int)
match_auto_data_df = match_auto_data_df.sort_values('mean_season_last_auto_points', ascending= False)
match_auto_data_df['rank'] = match_auto_data_df.groupby(['match_key','alliance']).cumcount() + 1
match_auto_data_df['rank'] = "team_key" + match_auto_data_df['rank'].astype(str)

slots_df = match_auto_data_df.pivot(index = ['match_key','alliance','auto_won', 'actual_time','auto_points'], columns = 'rank', values = 'team_key')

match_auto_data_df.drop(columns='rank')



stat_cols = [col for col in match_auto_data_df.columns
             if col not in ['team_key', 'match_key', 'actual_time', 'auto_points', 'alliance', 'opp_auto_points','rank', 'auto_won']]


for i, col in enumerate(['team_key1', 'team_key2', 'team_key3'],1):
    rename_dict = {col: f't{i}_{col}' for col in stat_cols}
    slots_df = slots_df.merge(
        match_auto_data_df.set_index(['team_key', 'match_key', 'alliance','auto_won','actual_time','auto_points'])[stat_cols],
        left_on = [col, 'match_key', 'alliance','auto_won','actual_time','auto_points'],
        right_index = True,
        how = 'left'
    ).rename(columns = rename_dict)
slots_df = slots_df.reset_index()

# # calculate mean and std for each future match
# model = joblib.load(MODEL_DIR / "20260521_1430_Auto_RegressionGBM_LARGE_RANGE.pk1")
model = joblib.load(auto_point_reg_gbm)
params = model.get_params()

feature_cols = [c for c in slots_df.columns if c.startswith(('t1_', 't2_', 't3_'))]


X = slots_df[feature_cols]
Y = slots_df['auto_points']

split_date = '2026-04-10'

train_mask = slots_df['actual_time'] < split_date
test_mask = slots_df['actual_time'] >= split_date

X_train = X[train_mask]
Y_train = Y[train_mask]
X_test = X[test_mask]
Y_test = Y[test_mask]

# X_train, X_test, Y_train, Y_test = split_train_test_data_from_target_column_feature_columns_and_date(slots_df,target_col='auto_points', date = split_date, feature_cols= feature_cols)

brier_score_df = slots_df[test_mask]
brier_score_df = brier_score_df[['match_key','alliance','team_key1','team_key2','team_key3','auto_won']]
brier_score_df['pred_auto_points'] = model.predict(X_test)

opp_df = brier_score_df.copy()
opp_df['alliance'] = opp_df['alliance'].map({'red': 'blue', 'blue': 'red'})
opp_df = opp_df.rename(columns={'pred_auto_points': 'opp_pred_auto_points'})
brier_score_df = brier_score_df.merge(opp_df[['match_key','alliance','opp_pred_auto_points']], on=['match_key', 'alliance'], how='left')



# calcling rmse of data
X_std_train = X_train[:int(len(X_train)*0.8)]
X_std_test = X_train[int(len(X_train)*0.8):]
Y_std_train = Y_train[:int(len(X_train)*0.8)]
Y_std_test = Y_train[int(len(X_train)*0.8):]
m = lgb.LGBMRegressor(**params)
m.fit(X_std_train, Y_std_train)
Y_std_pred = m.predict(X_std_test)
rmse = root_mean_squared_error(Y_std_test,Y_std_pred)

#calculate the change of each team winning
rmse_real = 6.3
brier_score_df['win_pct'] =1- norm.cdf(0, loc = brier_score_df['pred_auto_points'] - brier_score_df['opp_pred_auto_points'], scale = rmse_real * np.sqrt(2))

brier_score_df['pct_bin'] = pd.cut(brier_score_df['win_pct'], bins=10)



cal = brier_score_df.groupby('pct_bin', observed=True).agg(
    mean_pred=('win_pct', 'mean'),
    actual_win_rate=('auto_won', 'mean'),
    count=('auto_won', 'count')
).reset_index()

fig = px.scatter(cal, x='mean_pred', y='actual_win_rate', title='Auto Win Prediction Calibration (2026)',
                 color_discrete_sequence=['lightblue'],
                 labels={'mean_pred': 'predicted_win_rate', 'actual_win_rate': 'actual_win_rate'})
fig.update_traces(name='actual_win_rate', showlegend=True,
                  hovertemplate='mean_pred: %{x:.3f}<br>actual_win_rate: %{y:.3f}<extra></extra>')
fig.add_bar(x=cal['mean_pred'], y=cal['count'], opacity=0.3, name='sample count', yaxis='y2')
fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='ideal correlation',
                         line=dict(dash='dash', color='red')))

fig.update_layout(
    yaxis2=dict(title='sample count', overlaying='y', side='right', showgrid=False, range=[0, 4000], tickvals=[0, 800, 1600, 2400, 3200, 4000]),
    legend=dict(x=1.15, y=1)
)
st.plotly_chart(fig)

st.text(f"The brier_score is {brier_score_loss( brier_score_df['auto_won'], brier_score_df['win_pct']):.4f} and statbotics total match brier_score is ~0.180 (closer to 0 is better)")