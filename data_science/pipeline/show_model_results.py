import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import streamlit as st
import plotly.express as px


def print_rmse_and_mae(Y_pred:pd.DataFrame, Y_test:pd.DataFrame) -> None:
    print(f"MAE: {mean_absolute_error(Y_test, Y_pred):.2f}")
    print(f"RMSE: {root_mean_squared_error(Y_test, Y_pred):.2f}")


# @st.cache_data
def st_print_rmse_and_mae(Y_pred:pd.DataFrame, Y_test:pd.DataFrame) -> None:
    st.text(f"MAE: {mean_absolute_error(Y_test, Y_pred):.2f}")
    st.text(f"RMSE: {root_mean_squared_error(Y_test, Y_pred):.2f}")


# @st.cache_data
def st_plot_scatter_pred_vs_test(Y_pred:pd.DataFrame, Y_test:pd.DataFrame, *, title:str = "Predicted vs Actual Values", x_title:str = "Test Values", y_title:str = "Predicted Values") -> None:
    st.plotly_chart(px.scatter(x=Y_test, y=Y_pred, title = title, labels = {"x" : x_title, "y": y_title}))