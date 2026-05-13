import pandas as pd
import json
from pathlib import Path


from config import REPO_ROOT


DISTRICTS_FOLDER = REPO_ROOT / 'api' / 'json' / 'districts_data'
SAVE_PATH = REPO_ROOT / 'sql' / 'jsons_of_sql_tables'/ 'teams_numbers_by_year.json'



district_keys = set()
district_list_for_conv_df = []
district_files = [p.name for p in Path(DISTRICTS_FOLDER).iterdir() if p.is_file()]
for file_name in district_files:
        loop_path = DISTRICTS_FOLDER / file_name
        with open(loop_path) as loop_file:
              loop_data = json.load(loop_file)
        for districts_entry in loop_data:
                loop_key = districts_entry['key']
                loop_abbreviation = districts_entry['abbreviation']
                loop_full_name = districts_entry['display_name']
                district_list_for_conv_df.append({'districtKey':loop_key, 'districtCodes':loop_abbreviation,'districtName':loop_full_name})
                if loop_key in district_keys:
                        print(f"Error district key {loop_key} already exists")
                district_keys.add(loop_key)
                
district_df = pd.DataFrame(district_list_for_conv_df)
district_json = district_df.to_json(SAVE_PATH, orient = 'records', indent = 2)

