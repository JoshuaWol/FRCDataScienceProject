import time


from optuna.study import MaxTrialsCallback
from optuna.trial import TrialState
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
import joblib
import lightgbm as lgb
import numpy as np
import optuna
import optuna.visualization as vis
import plotly.express as px
import streamlit as st
import threading


from config import POSTGRESQL_OPTUNA_DB_URL, MODEL_DIR
from sql.load_db_to_df import load_df_from_db



# STUDY_NAME = 'Auto_RegressionGBM_Quad_Plot'
STUDY_NAME = 'Auto_RegressionGBM_LARGE_RANGE'
STORAGE_NAME = POSTGRESQL_OPTUNA_DB_URL
TARGET_MAX_TRIALS = 2435
TIME_STR =  time.strftime('%Y%m%d_%H%M',time.localtime())
FILE_MODEL_NAME = f"{TIME_STR}_{STUDY_NAME}.pk1"
MODEL_PATH = MODEL_DIR / FILE_MODEL_NAME


def objective(trial):
    params = {
    'num_leaves':         trial.suggest_int('num_leaves', 50, 130),
    'learning_rate':      trial.suggest_float('learning_rate', 0.01, 0.16, log=True),
    'min_child_samples':  trial.suggest_int('min_child_samples', 5, 60),
    'feature_fraction':   trial.suggest_float('feature_fraction', 0.5, 0.9),
    'bagging_fraction':   trial.suggest_float('bagging_fraction', 0.5, 0.9),
    'n_estimators':       500,
    'objective':          'regression',
    'verbose': -1,
}
    
    scores = []
    train_scores = []
    hold_test_scores = []
    for train_idx, val_idx in TimeSeriesSplit(n_splits=5).split(X_train):
        X_train_idx, X_val_idx = X_train.iloc[train_idx], X_train.iloc[val_idx]
        Y_train_idx, Y_val_idx = Y_train.iloc[train_idx], Y_train.iloc[val_idx]
        model = lgb.LGBMRegressor(**params, n_jobs = -1)
        model.fit(
             X_train_idx,  Y_train_idx,
            eval_set = [(X_val_idx, Y_val_idx)],
            callbacks = [lgb.early_stopping(50, verbose = False)]
        )

        val_preds = model.predict(X_val_idx)
        scores.append(mean_absolute_error(Y_val_idx,val_preds))

        train_preds = model.predict(X_train_idx)
        train_scores.append(mean_absolute_error(Y_train_idx,train_preds))
        hold_test_preds = model.predict(X_test)
        hold_test_scores.append(mean_absolute_error(Y_test, hold_test_preds))
    print(len(scores),len(train_scores),len(hold_test_scores))
    val_mae = sum(scores) / len(scores)
    train_mae = sum(train_scores) / len(train_scores)
    hold_test_mae = sum(hold_test_scores) / len(hold_test_scores)

    trial.set_user_attr('train_mae', train_mae)
    trial.set_user_attr('val_mae', val_mae)
    trial.set_user_attr('overfit_gap', train_mae - val_mae)
    trial.set_user_attr('hold_test_mae', hold_test_mae)
    
    return val_mae


_ctx = get_script_run_ctx()

def callback(study, trial):
    add_script_run_ctx(threading.current_thread(), _ctx)
    done = len(study.trials)
    progress.progress(min(done / TARGET_MAX_TRIALS, 1.0))
    status.text(f"Trial {done}/{TARGET_MAX_TRIALS} — best so far: {study.best_value:.4f}")


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


storage = optuna.storages.RDBStorage(
    url=STORAGE_NAME,
    engine_kwargs={
        "pool_pre_ping": True,
        "pool_recycle": 300,
    },
)
study = optuna.create_study(direction='minimize', study_name=STUDY_NAME, storage=storage, load_if_exists=True)
study.optimize(objective, n_trials = 2000, n_jobs = 4, show_progress_bar= True, callbacks = [callback, MaxTrialsCallback(TARGET_MAX_TRIALS, states = (TrialState.COMPLETE,))])


final_model = lgb.LGBMRegressor(**study.best_params).fit(X_train, Y_train)
test_preds = final_model.predict(X_test)
print(f"MAE on held-out test: {mean_absolute_error(Y_test, test_preds):.4f}")
print(f"RMSE on held-out test: {root_mean_squared_error(Y_test, test_preds):.4f}")

end_time = time.time()
print(start_time - end_time)

joblib.dump(final_model, MODEL_PATH)

st.plotly_chart(vis.plot_optimization_history(study))
st.plotly_chart(vis.plot_param_importances(study))
st.plotly_chart(vis.plot_slice(study))
st.text(f"MAE on held-out test: {mean_absolute_error(Y_test, test_preds):.4f}")
st.text(f"RMSE on held-out test: {root_mean_squared_error(Y_test, test_preds):.4f}")

scatter_test_pred_fig = px.scatter(x = Y_test, y = test_preds) 
st.plotly_chart(scatter_test_pred_fig)

user_attr_df = study.trials_dataframe()
user_attr_fig = px.line(data_frame = user_attr_df, x='number', y=['user_attrs_train_mae', 'user_attrs_val_mae', 'user_attrs_hold_test_mae', 'user_attrs_overfit_gap'], markers = True)
st.plotly_chart(user_attr_fig)

st.plotly_chart(vis.plot_parallel_coordinate(study))

# study = optuna.load_study(study_name='frc_lgbm', storage='sqlite:///study.db')
