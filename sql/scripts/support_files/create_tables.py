from pathlib import Path


from sql.data_science_db import get_psycopg_connection
from config import SCHEMA


with get_psycopg_connection() as conn, conn.cursor() as cur:
        cur.execute(f"SET search_path TO {SCHEMA}")
        SCRIPT_DIR = Path(Path(__file__).parent).parent
        SQL_SCHEMA_FILE = SCRIPT_DIR / "SQL_Schema.sql"
        cur.execute(Path(SQL_SCHEMA_FILE).read_text())

        if SCHEMA == 'production':
                cur.execute("SET search_path TO public")
        conn.commit()