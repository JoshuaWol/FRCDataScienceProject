#streamlit run test_streamlit_server.py --server.address=0.0.0.0 --server.port=8000
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from dython.nominal import associations
from config import IMPORTANT_FEATURES_PHASE, IMPORTANT_FEATURES
from data_science.data_science_functions import transform_shift_to_phase


from sql.data_science_db import get_sqlalchemy_connection

@st.cache_data
def load_features__matches_eda() -> pd.DataFrame:
    with get_sqlalchemy_connection() as conn:
        return pd.read_sql_table('matches_eda',con = conn,schema="features")

@st.cache_data
def load_schema_table(schema:str, table:str) -> pd.DataFrame:
    with get_sqlalchemy_connection() as conn:
        return pd.read_sql_table(table,con = conn,schema=schema)


@st.cache_data
def make_scatter(df:pd.DataFrame,x:str,y:str) -> px.scatter:
    return px.scatter( data_frame=df, x=x, y=y, render_mode="webgl")


@st.cache_data
def make_bar_list_y(df:pd.DataFrame,x:str,y:list[str],*,title:str = "Missing Values") -> px.bar:
    return px.bar( data_frame=df, x=x, y=y, orientation = 'v', barmode = 'group', title=title)

@st.cache_data
def make_bar_plot(df:pd.DataFrame,x:str,y:str,*,title:str = "Missing Values") -> px.bar:
    return px.bar( data_frame=df, x=x, y=y, orientation = 'v', barmode = 'group', title=title)

@st.cache_data
def make_box_plot(df:pd.DataFrame,y:list[str],*,title:str = "Missing Values"):
    return px.box( data_frame=df, y=y, title=title)




matches_eda_df = load_features__matches_eda()
matches_eda_df = matches_eda_df[IMPORTANT_FEATURES]

matches_eda_df = transform_shift_to_phase(matches_eda_df)


matches_eda_df_cols_num = matches_eda_df.select_dtypes(include="number").columns.tolist()
x_axis_selection = st.selectbox("X axis", matches_eda_df_cols_num)
y_axis_selection = st.selectbox("Y axis",matches_eda_df_cols_num)
# st.scatter_chart(data=matches_eda_df,x=x_axis_selection, y=y_axis_selection )
# st.plotly_chart(make_scatter(matches_eda_df,x_axis_selection,y_axis_selection),width='stretch')



schema_table_dict = {'features': ['matches_eda'],'public':['districts','events','match_data_2026','match_teams','matches','teams']}
for schema in schema_table_dict:
    for table in schema_table_dict[schema]:
        df = load_schema_table(schema, table)
        df_cols = df.columns.tolist()
        null_list = []
        not_null_list = []
        null_col_list = []
        for curr_column in df_cols:
            null_count = df[curr_column].isnull().sum()
            not_null_count = df[curr_column].count()
            if null_count != 0:
                null_list.append(null_count)
                not_null_list.append(not_null_count)
                null_col_list.append(curr_column)
        null_col_df = pd.DataFrame({
            'column': null_col_list,
            'null_count': null_list,
            'not_null_count' : not_null_list,
        })
        if len(null_col_df) >0:
            long_df = null_col_df.melt(id_vars = 'column', value_vars = ['null_count','not_null_count'], var_name = "metric", value_name = 'count')
            long_df['pct'] = long_df.groupby('column')['count'].transform(lambda v: v/v.sum() *100)
            fig = px.bar(data_frame=long_df, x='column', y='count', color = 'metric', barmode = 'group', orientation = 'v', title=f"Missing values in {schema}.{table}",
                        text=long_df['pct'].round(1).astype(str) +'%')
            st.plotly_chart(fig)
        else:
            st.text(f"**No missing values in {schema}.{table}**")


##Box Plots of all data
# # std_matches_eda_df = matches_eda_df.select_dtypes(include = 'number').std()
# st.plotly_chart(make_box_plot(matches_eda_df.select_dtypes(include = 'number'), matches_eda_df_cols_num, title='Box Plot to look for Outliers' ))
# # matches_eda_df.select_dtypes(include = 'number')

# matches_eda_df_num = matches_eda_df[matches_eda_df_cols_num]
# z_matches_eda_df = (matches_eda_df_num - matches_eda_df_num.mean())/matches_eda_df_num.std()
# st.plotly_chart(make_box_plot(z_matches_eda_df, matches_eda_df_cols_num, title='Normalized Box Plot to look for Outliers' ))




# ###Correlation Matrices
# exclude = ['match_key','team_key1','team_key2','team_key3','event_key']
# df_for_corr = matches_eda_df.drop(columns = exclude)
# df_encoded = pd.get_dummies(df_for_corr, drop_first = False)
# corr = df_encoded.corr(method = 'pearson')
# st.text('Pearson Correlation')
# # fig1 = px.imshow(corr,
# #                 color_continuous_scale='RdBu_r',
# #                 zmin=-1, zmax=1,
# #                 aspect='auto',
# #                 text_auto='.2f',)
# # st.plotly_chart(fig1, width = 'stretch')

# corr_spearman = df_encoded.corr(method = 'spearman')
# # fig2 = px.imshow(corr_spearman,
# #                 color_continuous_scale='RdBu_r',
# #                 zmin=-1, zmax=1,
# #                 aspect='auto',
# #                 text_auto='.2f',)
# # st.text('Spearman Correlation')
# # st.plotly_chart(fig2, width = 'stretch')

# corr_delta = corr - corr_spearman
# st.text('Pearson - Spearman Correlation Delta')
# # fig3 = px.imshow(corr_delta,
# #                 color_continuous_scale='RdBu_r',
# #                 zmin=-1, zmax=1,
# #                 aspect='auto',
# #                 text_auto='.2f',)
# # st.plotly_chart(fig3, width = 'stretch')


# ## correlation using pands
# # df_combined = pd.DataFrame()
# # df_combined['pearson'] = corr['total_score']
# # df_combined['spearman']=corr_spearman['total_score']
# # df_combined['delta (pearson-spearman)'] = corr['total_score'] - corr_spearman['total_score']
# # # st.dataframe(corr['total_score'].sort_values(ascending=False))
# # st.text("Total_Score Correlations by Method")
# # # st.dataframe(df_combined)
# # df_combined_reset = df_combined.reset_index()
# # df_combined_melt = df_combined_reset.melt(id_vars= 'index', value_vars = ['pearson', 'spearman', 'delta (pearson-spearman)'], var_name = 'Corr Method', value_name = 'Correlation' )
# # # long_df = null_col_df.melt(id_vars = 'column', value_vars = ['null_count','not_null_count'], var_name = "metric", value_name = 'count')
# # print(df_combined_melt)
print('starting')
matches_eda_df_associations = matches_eda_df.dropna(axis=0)
dyt_pearson = associations(matches_eda_df_associations, num_num_assoc = 'pearson', plot = 'False')
dyt_spearman = associations(matches_eda_df_associations, num_num_assoc = 'spearman', plot = 'False')

print('associated')
dyt_combined = pd.DataFrame()
dyt_combined['spearman'] = dyt_spearman['corr']['total_score'].drop('total_score')
dyt_combined['pearson'] = dyt_pearson['corr']['total_score'].drop('total_score')
dyt_combined['spearman-pearson'] = dyt_combined['spearman'] - dyt_combined['pearson']
dyt_combined.sort_values(by = ['spearman', 'spearman-pearson'], ascending = False, inplace = True )
dyt_combined.reset_index(inplace= True)
print('combined')
st.plotly_chart(make_bar_list_y(dyt_combined, 'index', ['spearman', 'pearson', 'spearman-pearson'], title='Barchart of Association(corr) Values per column'))
print('done')

print(dyt_combined[dyt_combined['spearman'] >= 0.3]['index'].tolist())