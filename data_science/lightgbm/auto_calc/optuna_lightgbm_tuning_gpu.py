import time
from sklearnex import patch_sklearn
patch_sklearn()


import lightgbm as lgb
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
import threading
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
import plotly.express as px
import optuna.visualization as vis
import optuna

from sql.load_db_to_df import load_df_from_db


def objective(trial):
    params = {
    'num_leaves':         trial.suggest_int('num_leaves', 15, 63),
    'learning_rate':      trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
    'min_child_samples':  trial.suggest_int('min_child_samples', 50, 500),
    'feature_fraction':   trial.suggest_float('feature_fraction', 0.6, 0.9),
    'bagging_fraction':   trial.suggest_float('bagging_fraction', 0.6, 0.9),
    # 'bagging_freq':       trial.suggest_int('bagging_freq', 0, 7),   Features < 0.01
    # 'reg_alpha':          trial.suggest_float('reg_alpha', 1e-8, 10, log=True),  Features <0.01
    # 'reg_lambda':         trial.suggest_float('reg_lambda', 1e-8, 10, log=True), Features <0.01
    'n_estimators':       2000,
    'objective':          'regression',
    'device': 'gpu',
    'gpu_platform_id': 0,
    'gpu_device_id': 0,
    # 'random_state':       42,
    'verbose': -1,
}
    
    scores = []
    for train_idx, val_idx in TimeSeriesSplit(n_splits=5).split(X_train):
        model = lgb.LGBMRegressor(**params, n_jobs = -1).fit(
            X_train.iloc[train_idx], Y_train.iloc[train_idx],
            eval_set = [(X_train.iloc[val_idx], Y_train.iloc[val_idx])],
            callbacks = [lgb.early_stopping(50, verbose = False)]
        )
        preds = model.predict(X_train.iloc[val_idx])
        scores.append(mean_absolute_error(Y_train.iloc[val_idx],preds))
    return sum(scores)/ len(scores)


_ctx = get_script_run_ctx()

def callback(study, trial):
    add_script_run_ctx(threading.current_thread(), _ctx)
    progress.progress((trial.number + 1) / 100)
    status.text(f"Trial {trial.number+1}/100 — best so far: {study.best_value:.4f}")


progress = st.progress(0)
status = st.empty()

match_data_df = load_df_from_db('features', 'match_auto_data_calc')

start_time = time.time()
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
Y_train = Y[train_mask]
X_test = X[test_mask]
Y_test = Y[test_mask]


study = optuna.create_study(direction = 'minimize')
study.optimize(objective, n_trials = 100, n_jobs = 1, show_progress_bar= True, callbacks = [callback])


final_model = lgb.LGBMRegressor(**study.best_params).fit(X_train, Y_train)
test_preds = final_model.predict(X_test)
print(f"MAE on held-out test: {mean_absolute_error(Y_test, test_preds):.4f}")
print(f"RMSE on held-out test: {root_mean_squared_error(Y_test, test_preds):.4f}")

st.plotly_chart(vis.plot_optimization_history(study))
st.plotly_chart(vis.plot_param_importances(study))
st.plotly_chart(vis.plot_parallel_coordinate(study))
st.plotly_chart(vis.plot_slice(study))
st.text(f"MAE on held-out test: {mean_absolute_error(Y_test, test_preds):.4f}")
st.text(f"RMSE on held-out test: {root_mean_squared_error(Y_test, test_preds):.4f}")


# study = optuna.load_study(study_name='frc_lgbm', storage='sqlite:///study.db')

end_time = time.time()
print(start_time - end_time)