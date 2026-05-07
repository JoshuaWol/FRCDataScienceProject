from pathlib import Path


from sql.data_science_db import get_psycopg_connection

with get_psycopg_connection() as conn, conn.cursor() as cur:
        SCRIPT_DIR = Path(Path(__file__).parent).parent
        SQL_SCHEMA_FILE = SCRIPT_DIR / "SQL_Schema.sql"
        cur.execute(Path(SQL_SCHEMA_FILE).read_text())
        conn.commit()