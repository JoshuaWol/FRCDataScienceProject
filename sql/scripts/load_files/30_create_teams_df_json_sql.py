import pandas as pd
import json
from pathlib import Path


from sql.write_df_to_sql import write_df_to_postgres
from sql.get_keys_from_table import get_keys_from_table_schema_set
from config import REPO_ROOT, SCHEMA


TEAMS_FOLDER = REPO_ROOT / 'api' / 'json' / 'teams_data'
SAVE_PATH = REPO_ROOT / 'sql' / 'jsons_of_sql_tables'/ 'teams_in_frc.json'


existing_team_keys_set = get_keys_from_table_schema_set('team_key','teams',SCHEMA)



team_list_for_conv_df = []
team_paths = [p for p in Path(TEAMS_FOLDER).iterdir() if p.is_file()]
for loop_path in team_paths:
        with open(loop_path) as loop_file:
              loop_data = json.load(loop_file)
        for teams_entry in loop_data:
                loop_team_key = teams_entry['key']
                if loop_team_key not in  existing_team_keys_set:
                    team_list_for_conv_df.append({
                            'team_key':loop_team_key,
                            'team_number':teams_entry['team_number'],
                            'name_full':teams_entry.get('name'),
                            'rookie_year':teams_entry.get('rookie_year'),
                            'city': teams_entry.get('city'),
                            'state_prov': teams_entry.get('state_prov'),
                            'country': teams_entry.get('country'),
                            'postal_code':teams_entry.get('postal_code'),
                            })
                existing_team_keys_set.add(loop_team_key)
                
team_df = pd.DataFrame(team_list_for_conv_df)
team_json = team_df.to_json(SAVE_PATH, orient = 'records', indent = 2)

write_df_to_postgres(team_df, 'teams', if_exists = "append", schema = SCHEMA)
