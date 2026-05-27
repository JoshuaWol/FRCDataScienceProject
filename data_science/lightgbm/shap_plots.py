import pandas as pd
import numpy as np
import joblib
import streamlit as st
import shap
import matplotlib.pyplot as plt
import json


from sql.load_db_to_df import load_df_from_db
from config import auto_point_reg_gbm, SHAP_DIR, auto_point_reg_gbm_file



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


def dark_plots(func):
    def wrapper(*args, **kwargs):
        with plt.style.context(['dark_background', {'text.color': "#f3ecec", 'axes.labelcolor': '#e0e0e0', 'xtick.color': '#e0e0e0', 'ytick.color': '#e0e0e0'}]):
            return func(*args, **kwargs)
    return wrapper

@dark_plots
def plot_shap(shap_values:shap, plot_type:str,  **kwargs):
    fig, ax = plt.subplots()
    plot_func = getattr(shap.plots, plot_type)
    if plot_type == 'waterfall':
        plot_func(shap_values[kwargs.get('index', 0)], show=False)
    elif plot_type == 'scatter':
        plot_func(shap_values[:, kwargs['feature']], show=False)
    else:
        plot_func(shap_values, show=False, **{k: v for k, v in kwargs.items() if k != 'index'})
        if len(plt.gca().get_yticklabels()) > 0 :
            for label in plt.gca().get_yticklabels():
                label.set_color('#e0e0e0')
    st.pyplot(fig); plt.close(fig)

@dark_plots
def plot_shap_summary(shap_values, X_test, **kwargs):
    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, X_test, show=False, **{k: v for k, v in kwargs.items() if k != 'index'})
    for label in plt.gca().get_yticklabels():
        label.set_color('#e0e0e0')
    st.pyplot(fig); plt.close(fig)


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