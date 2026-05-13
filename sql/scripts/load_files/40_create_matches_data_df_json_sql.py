import pandas as pd
import json
from pathlib import Path


from sql.write_df_to_sql import write_df_to_postgres #noqa
from sql.match_data_from_json import matches_teams_from_json, matches_from_json, matches_data_2026_from_json
from sql.get_keys_from_table import get_keys_from_table_schema_set
from config import REPO_ROOT, SCHEMA


MATCHES_FOLDER = REPO_ROOT / 'api' / 'json' / 'matches_data'
MATCH_DATA_SAVE_PATH = REPO_ROOT / 'sql' / 'jsons_of_sql_tables'/ 'matches_data_in_frc.json'
MATCH_TEAMS_SAVE_PATH = REPO_ROOT / 'sql' / 'jsons_of_sql_tables'/ 'matches_teams_in_frc.json'



existing_match_keys_match_data_set = get_keys_from_table_schema_set('match_key', 'match_data_2026', SCHEMA)
existing_match_keys_match_teams_set = get_keys_from_table_schema_set('match_key', 'match_teams', SCHEMA)
existing_match_keys_matches_set = get_keys_from_table_schema_set('match_key', 'matches', SCHEMA)


match_key = set()
matches_teams_for_conv_df = []
matches_data_for_conv_df = []
matches_for_conv_df = []
paths_for_loop = [p for p in Path(MATCHES_FOLDER).glob("*2026*") if p.is_file()]
for loop_path in paths_for_loop:
    with open(loop_path) as loop_file:
        loop_data = json.load(loop_file)
    for matches_entry in loop_data:
            loop_match_key = matches_entry['key']
            if loop_match_key not in existing_match_keys_match_data_set:
                matches_data_for_conv_df.extend(matches_data_2026_from_json(matches_entry))
            if loop_match_key not in existing_match_keys_match_teams_set:
                matches_teams_for_conv_df.extend(matches_teams_from_json(matches_entry))
            if loop_match_key not in existing_match_keys_matches_set:
                matches_for_conv_df.extend(matches_from_json(matches_entry))
            existing_match_keys_match_data_set.add(loop_match_key)
            existing_match_keys_match_teams_set.add(loop_match_key)
            existing_match_keys_matches_set.add(loop_match_key)
                
matches_data_df = pd.DataFrame(matches_data_for_conv_df)
matches_teams_df = pd.DataFrame(matches_teams_for_conv_df)
matches_df = pd.DataFrame(matches_for_conv_df)
matches_data_json = matches_data_df.to_json(MATCH_DATA_SAVE_PATH, orient = 'records', indent = 2)
matches_teams_json = matches_teams_df.to_json(MATCH_TEAMS_SAVE_PATH, orient = 'records', indent = 2)


schema = "public"
if_exists = "append"
write_df_to_postgres(matches_df, 'matches', if_exists = if_exists, schema = SCHEMA)
write_df_to_postgres(matches_data_df, 'match_data_2026', if_exists = if_exists , schema = SCHEMA)
write_df_to_postgres(matches_teams_df, 'match_teams', if_exists = if_exists, schema = SCHEMA)
