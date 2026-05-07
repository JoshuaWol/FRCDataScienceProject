import pandas as pd
from sql.data_science_db import get_sqlachemy_connection

def write_df_to_postgres ( data_frame: pd.DataFrame, sql_table_name: str, if_exists_action : str = "fail") -> None:
    with get_sqlachemy_connection() as sql_conn:
        data_frame.to_sql(
            name = sql_table_name,
            con = sql_conn,
            if_exists = if_exists_action,
            index = False,
            method = 'multi',
            chunksize = 300

        )