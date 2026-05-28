import pandas as pd
import streamlit as st
import shap
import matplotlib.pyplot as plt


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