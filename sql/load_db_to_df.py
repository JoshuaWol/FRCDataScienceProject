import pandas as pd


from sql.data_science_db import get_sqlalchemy_connection


def load_df_from_db(schema:str, table:str) -> pd.DataFrame:
    with get_sqlalchemy_connection() as conn:
        return pd.read_sql_table(table,con = conn,schema=schema)