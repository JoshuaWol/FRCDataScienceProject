#streamlit run test_streamlit_server.py --server.address=0.0.0.0 --server.port=8000
import streamlit as st
import plotly.express as px
import pandas as pd


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
def make_bar_two_y(df:pd.DataFrame,x:str,y:list[str],*,title:str = "Missing Values") -> px.bar:
    return px.bar( data_frame=df, x=x, y=y, orientation = 'v', barmode = 'group', title=title)

@st.cache_data
def make_bar_plot(df:pd.DataFrame,x:str,y:str,*,title:str = "Missing Values") -> px.bar:
    return px.bar( data_frame=df, x=x, y=y, orientation = 'v', barmode = 'group', title=title)

matches_eda_df = load_features__matches_eda()

matches_eda_df_cols_num = matches_eda_df.select_dtypes(include="number").columns.tolist()
x_axis_selection = st.selectbox("X axis", matches_eda_df_cols_num)
y_axis_selection = st.selectbox("Y axis",matches_eda_df_cols_num)
# st.scatter_chart(data=matches_eda_df,x=x_axis_selection, y=y_axis_selection )
st.plotly_chart(make_scatter(matches_eda_df,x_axis_selection,y_axis_selection),width='stretch')



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

# print(matches_eda_df.loc[matches_eda_df['predicted_time'].isnull()][['event_key','event_type','actual_time', 'district_key']])

st.dataframe(matches_eda_df.loc[matches_eda_df['predicted_time'].isnull()][['predicted_time','event_key','event_type','actual_time', 'district_key','match_key']])

