import lightgbm as lgb
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import streamlit as st
import plotly.express as px

from sql.load_db_to_df import load_df_from_db
from data_science.pipeline.split_train_test_data import split_train_test_data_from_target_column_feature_columns_and_date
from data_science.pipeline.show_model_results import print_rmse_and_mae, st_print_rmse_and_mae, st_plot_scatter_pred_vs_test
from data_science.pipeline.combine_and_sort_teams_in_alliance_based_on_target_col import combine_and_sort_teams_in_alliance_based_on_target_col_and_match_key

match_data_df = load_df_from_db('features', 'match_auto_data_calc')

wide_df = combine_and_sort_teams_in_alliance_based_on_target_col_and_match_key(match_data_df, 'mean_season_last_auto_points', index =  ['match_key','alliance', 'actual_time','auto_points'],
                                                                                non_stats_cols=['team_key', 'match_key', 'actual_time', 'auto_points', 'alliance', 'opp_auto_points','rank', 'auto_won'] )

feature_cols = [c for c in wide_df.columns if c.startswith(('t1_', 't2_', 't3_'))]
split_date = '2026-04-10'
X_train, X_test, Y_train, Y_test = split_train_test_data_from_target_column_feature_columns_and_date(wide_df, target_col = 'auto_points', feature_cols=feature_cols, date=split_date )

model = lgb.LGBMRegressor(
    objective='regression',
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=33,
    n_jobs=1,
)

model.fit(X_train, Y_train, eval_set=[(X_test, Y_test)])

Y_pred = model.predict(X_test)
print_rmse_and_mae(Y_pred, Y_test)
st_print_rmse_and_mae(Y_pred, Y_test)
st_plot_scatter_pred_vs_test(Y_pred, Y_test)
