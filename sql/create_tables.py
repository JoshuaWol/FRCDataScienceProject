from pathlib import Path


from sql.data_science_db import get_connection

with get_connection() as conn, conn.cursor() as cur:
        SCRIPT_DIR = Path(__file__).parent
        SQL_SCHEMA_FILE = SCRIPT_DIR / "SQL_Schema.sql"
        cur.execute(Path(SQL_SCHEMA_FILE).read_text())
        conn.commit()