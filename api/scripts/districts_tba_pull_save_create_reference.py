import json


from api.frc_and_tba_api_url_builders import build_tba_districts_url
from api.pull_and_save_api_url_data import pull_and_save_tba_api_data
from config import REPO_ROOT, START_YEAR, END_YEAR

DISTRICTS_FOLDER = REPO_ROOT / 'api' / 'json' / 'districts_data'
SAVE_FOLDER = REPO_ROOT / 'api' / 'json' / 'reference_data'
SAVE_FILE = "district_keys_by_year.json"
SAVE_PATH = SAVE_FOLDER / SAVE_FILE



for loop_year in range(START_YEAR,END_YEAR-1,-1):
    tba_district_api_url = build_tba_districts_url(loop_year)
    pull_and_save_tba_api_data(tba_district_api_url)





district_key_dict_by_year = {}
for loop_year in range(START_YEAR,END_YEAR-1,-1):
    file_name = f"districts|{loop_year}.json"
    folder_and_file_path = DISTRICTS_FOLDER / file_name 
    with open(folder_and_file_path) as file:
        json_data = json.load(file)

    district_keys = []
    for i in range(len(json_data)):
        curr_dict = json_data[i]
        district_keys.append(curr_dict["key"])
    district_key_dict_by_year[loop_year] = district_keys
with open(SAVE_PATH, 'w') as save_file:
    json.dump(district_key_dict_by_year, save_file, indent = 2)