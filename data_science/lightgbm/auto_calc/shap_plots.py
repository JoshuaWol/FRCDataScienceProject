import pandas as pd
import numpy as np
import joblib
import streamlit as st
import shap
import matplotlib.pyplot as plt
import json


from sql.load_db_to_df import load_df_from_db
from config import auto_point_reg_gbm, SHAP_DIR, auto_point_reg_gbm_file
from data_science.pipeline.combine_and_sort_teams_in_alliance_based_on_target_col import combine_and_sort_teams_in_alliance_based_on_target_col_and_match_key
from data_science.pipeline.split_train_test_data import split_train_test_data_from_target_column_feature_columns_and_date
from data_science.pipeline.shap_plots_functions import plot_shap, plot_shap_summary




#import best parameters from optuna study and sql data
match_auto_data_df = load_df_from_db(schema = 'features', table = 'match_auto_data_calc')
match_auto_data_df['auto_won'] = (match_auto_data_df['auto_points'] > match_auto_data_df['opp_auto_points']).astype(int)

slots_df = combine_and_sort_teams_in_alliance_based_on_target_col_and_match_key(match_auto_data_df, 'mean_season_last_auto_points')

# # calculate mean and std for each future match
model = joblib.load(auto_point_reg_gbm)
params = model.get_params()

feature_cols = [c for c in slots_df.columns if c.startswith(('t1_', 't2_', 't3_'))]
split_date = '2026-04-10'
X_train, X_test, Y_train, Y_test = split_train_test_data_from_target_column_feature_columns_and_date(slots_df, target_col='auto_points', feature_cols=feature_cols, date= split_date)

explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)


plot_shap_summary(shap_values, X_test, max_display=len(X_test.columns))        
plot_shap(shap_values, 'waterfall')
plot_shap(shap_values, 'bar', max_display=len(X_test.columns))
plot_shap(shap_values, 'beeswarm')

# shap_values from shap.Explainer(model)(X)  -> Explanation object
mean_abs = np.abs(shap_values.values).mean(axis=0).round(4)

importance_mean = pd.Series(mean_abs, index=shap_values.feature_names).sort_values(ascending=False)
print(importance_mean)

max_abs = np.abs(shap_values.values).max(axis = 0).round(4)
importance_max = pd.Series(max_abs, index = shap_values.feature_names).sort_values(ascending = False)
print(importance_max)

dict_for_json = {'max': importance_max.to_dict(), 'mean': importance_mean.to_dict()}

file_split = auto_point_reg_gbm_file.split('.')
file_name = file_split[0] + '.json'
with open(SHAP_DIR / file_name, 'w') as file:
    json.dump(dict_for_json, file)
