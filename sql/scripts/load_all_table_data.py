import subprocess
import sys
from pathlib import Path


from config import REPO_ROOT, DATABASE_URL

SCRIPT_DIR = Path(__file__).resolve().parent


file_load_list = ["create_districts_df_json_sql.py", 'create_events_df_json_sql.py','create_teams_df_json_sql.py','create_matches_data_df_json_sql.py']
for file_name in file_load_list:
    subprocess.run([sys.executable, SCRIPT_DIR / file_name], check=True)

subprocess.run(['psql', DATABASE_URL, '-f', REPO_ROOT / 'sql' / 'features' / "add_matches_eda_data.sql" ], check=True)
