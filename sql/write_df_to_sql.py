import pandas as pd
from sql.data_science_db import get_sqlalchemy_connection
from confirm import confirm

def write_df_to_postgres ( data_frame: pd.DataFrame, table: str, *, if_exists:str = "fail", schema: str = 'public') -> None:
    if schema == "production":
        if not confirm("This is writing into the PRODUCTION schema db, do you want to continue?"):
            print('db function cancelled.')
            return
        
    with get_sqlalchemy_connection() as sql_conn:
        data_frame.to_sql(
            name = table,
            con = sql_conn,
            if_exists = if_exists,
            schema = schema,
            index = False,
            method = 'multi',
            chunksize = 300

        )