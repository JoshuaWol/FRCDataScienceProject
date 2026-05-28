import warnings
import streamlit as st
import streamlit.elements.lib.utils as _st_utils
_st_utils.check_cache_replay_rules = lambda: None
st._config.set_option("client.showErrorDetails", "none")
st.markdown(
    "<style>div[data-testid='stException']{display:none;}</style>",
    unsafe_allow_html=True,
)

@st.cache_data()
def run_shap():
    exec(open("data_science/lightgbm/auto_calc/shap_plots.py").read(),globals())

@st.cache_data()
def run_brier_score():
    exec(open("data_science/lightgbm/auto_calc/brier_score_lightgbm.py").read(),globals())

@st.cache_data()
def run_lightgbm_fit():
    exec(open("data_science/lightgbm/auto_calc/optuna_lightgbm_tuning.py").read(),globals())

@st.cache_data()
def run_feature_check():
    exec(open("data_science/eda/test_streamlit_server.py").read(),globals())


tab1, tab2, tab3= st.tabs(['Checking Data', ' Fitting Data', 'Results'])


with tab1:
    run_feature_check()

with tab2:
    run_lightgbm_fit()

with tab3:
    run_brier_score()
    run_shap()


