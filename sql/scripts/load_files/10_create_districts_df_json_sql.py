import pandas as pd
import json
from pathlib import Path


from sql.write_df_to_sql import write_df_to_postgres
from sql.get_keys_from_table import get_keys_from_table_schema_set
from config import REPO_ROOT, SCHEMA


DISTRICTS_FOLDER = REPO_ROOT / 'api' / 'json' / 'districts_data'
SAVE_PATH = REPO_ROOT / 'sql' / 'jsons_of_sql_tables'/ 'teams_numbers_by_year.json'


existing_district_key_set = get_keys_from_table_schema_set('district_key', 'districts', SCHEMA)


district_list_for_conv_df = []
district_files = [p.name for p in Path(DISTRICTS_FOLDER).iterdir() if p.is_file()]
for file_name in district_files:
        loop_path = DISTRICTS_FOLDER / file_name
        with open(loop_path) as loop_file:
              loop_data = json.load(loop_file)
        for districts_entry in loop_data:
                loop_key = districts_entry['key']
                if loop_key not in existing_district_key_set:
                        loop_abbreviation = districts_entry['abbreviation']
                        loop_full_name = districts_entry['display_name']
                        district_list_for_conv_df.append({'district_key':loop_key, 'district_code':loop_abbreviation,'district_name':loop_full_name})
                existing_district_key_set.add(loop_key)
                
district_df = pd.DataFrame(district_list_for_conv_df)
district_json = district_df.to_json(SAVE_PATH, orient = 'records', indent = 2)

write_df_to_postgres(district_df, 'districts', if_exists = "append", schema = SCHEMA)

