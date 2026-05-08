import json
from pathlib import Path


from sql.data_science_db import get_psycopg_connection
from config import REPO_ROOT


TEAMS_FOLDER = REPO_ROOT / 'api' / 'json' / 'teams_data'
SAVE_PATH = REPO_ROOT / 'sql' / 'jsons_of_sql_tables'/ 'teams_in_frc.json'

team_numbers = set()
team_list_info = []
team_files = [p.name for p in Path(TEAMS_FOLDER).iterdir() if p.is_file()]
for file_name in team_files:
        loop_path = TEAMS_FOLDER / file_name
        district_code = file_name.split('|')[2][4:]
        with open(loop_path) as loop_file:
              loop_data = json.load(loop_file)
        for teams_entry in loop_data:
                loop_team_number = teams_entry['team_number']
                if loop_team_number not in team_numbers:
                    team_list_info.append({
                            'team_key':teams_entry['key'],
                            'name_short':teams_entry['nickname'],
                            })
                team_numbers.add(loop_team_number)
                

with get_psycopg_connection() as conn:
        for curr_team in team_list_info:
            team_key =  curr_team['team_key']
            name_short = curr_team['name_short']
            conn.execute("SET search_path TO production")
            conn.execute("UPDATE teams SET name_short = %(name_short)s where team_key = %(team_key)s", {"name_short": name_short, "team_key": team_key})
            conn.execute("SET search_path TO public")
        conn.commit()