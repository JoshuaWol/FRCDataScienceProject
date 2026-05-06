import json
from pathlib import Path
import subprocess

REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DISTRICS_FOLDER = REPO_ROOT / 'api' / 'json' / 'districts_data'
SAVE_FOLDER = REPO_ROOT / 'api' / 'json' / 'reference_data'
SAVE_FILE = "district_keys_by_year.json"
SAVE_PATH = SAVE_FOLDER / SAVE_FILE


district_key_dict_by_year = {}
for loop_year in range(2026,2009,-1):
    file_name = f"districts|{loop_year}.json"
    folder_and_file_path = DISTRICS_FOLDER / file_name 
    with open(folder_and_file_path) as file:
        json_data = json.load(file)

    district_keys = []
    for i in range(len(json_data)):
        curr_dict = json_data[i]
        district_keys.append(curr_dict["key"])
    district_key_dict_by_year[loop_year] = district_keys
print(len(district_key_dict_by_year[2026]))
with open(SAVE_PATH, 'w') as save_file:
    json.dump(district_key_dict_by_year, save_file, indent = 2)

