from sql.data_science_db import get_connection

with get_connection() as conn, conn.cursor() as cur:
        cur.execute(TABLES * FROM FRCDataScienceDB)