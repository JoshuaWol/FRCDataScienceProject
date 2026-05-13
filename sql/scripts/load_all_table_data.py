import subprocess
import sys
from pathlib import Path


from config import REPO_ROOT, DATABASE_URL, PY_LOAD_DIR, SQL_LOAD_DIR

# SCRIPT_DIR = Path(__file__).resolve().parent


# file_load_list = ["create_districts_df_json_sql.py", 'create_events_df_json_sql.py','create_teams_df_json_sql.py','create_matches_data_df_json_sql.py']
py_file_load_list = sorted([p for p in Path(PY_LOAD_DIR).iterdir() if p.is_file()])
for file_path in py_file_load_list:
    subprocess.run([sys.executable, file_path], check=True)

sql_file_load_list = sorted([p for p in Path(SQL_LOAD_DIR).iterdir() if p.is_file()])
for file_path in sql_file_load_list:
    subprocess.run(['psql', DATABASE_URL, '-f', file_path ], check=True)
