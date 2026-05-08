
def get_keys_from_table_schema_set(key_col:str, table:str, schema:str = 'public') -> list:
    from sql.data_science_db import get_psycopg_connection
    with get_psycopg_connection() as conn:
            existing_team_keys_list = conn.execute(f"SELECT {key_col} FROM {schema}.{table}" )
            conn.commit()
            return set([row[0] for row in existing_team_keys_list])