from collections import defaultdict

import json
from pathlib import Path


from api.frc_and_tba_api_url_builders import build_tba_matches_from_event_key_url
from api.pull_and_save_api_url_data import pull_and_save_tba_api_data
from config import REPO_ROOT, START_YEAR, END_YEAR

EVENTS_FOLDER = REPO_ROOT / 'api' / 'json' / 'events_data'
MATCHES_FOLDER = REPO_ROOT / 'api' / 'json' / 'matches_data'
EVENT_REFERENCE_FILE = REPO_ROOT / 'api' / 'json' / 'reference_data' / "event_keys_by_year.json"
SAVE_PATH = REPO_ROOT / 'api' / 'json' / 'reference_data'/ 'matches_numbers_by_year.json'


with open(EVENT_REFERENCE_FILE) as event_reference_file:
    event_reference_dict = json.load(event_reference_file)
for loop_year in range(START_YEAR,END_YEAR-1,-1):
    event_key_list = event_reference_dict[str(loop_year)]
    print(loop_year)
    for event_key in event_key_list:
        tba_match_api_url = build_tba_matches_from_event_key_url(event_key)
        pull_and_save_tba_api_data(tba_match_api_url)





matches_numbers_dict_by_year_set_dict = defaultdict(set)
match_files = [p.name for p in Path(MATCHES_FOLDER).iterdir() if p.is_file()]
for file_name in match_files:
    print(file_name)
    folder_and_file_path = MATCHES_FOLDER / file_name
    file_name_split = file_name.split('|')
    loop_year = file_name_split[2][:4]
    with open(folder_and_file_path) as file:
        json_data = json.load(file)

    match_number_list = []
    for i in range(len(json_data)):
        curr_dict = json_data[i]
        match_number = curr_dict["match_number"]
        match_number_list.append(match_number)
    matches_numbers_dict_by_year_set_dict[loop_year].update(match_number_list)

matches_numbers_dict_by_year_list_dict = {}
for key in matches_numbers_dict_by_year_set_dict:
    values = matches_numbers_dict_by_year_set_dict[key]
    values_list = list(values)
    values_list_ordered = sorted(values_list)
    matches_numbers_dict_by_year_list_dict[key] = values_list_ordered

with open(SAVE_PATH, 'w') as save_file:
    json.dump(matches_numbers_dict_by_year_list_dict, save_file, indent = 2)