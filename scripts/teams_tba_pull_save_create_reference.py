from collections import defaultdict

import json
from pathlib import Path
import subprocess


from api.frc_and_tba_api_url_builders import *
from api.pull_and_save_api_url_data import *


REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
EVENTS_FOLDER = REPO_ROOT / 'api' / 'json' / 'events_data'
TEAMS_FOLDER = REPO_ROOT / 'api' / 'json' / 'teams_data'
DISTRICT_REFERENCE_FILE = REPO_ROOT / 'api' / 'json' / 'reference_data' / "district_keys_by_year.json"
SAVE_PATH = REPO_ROOT / 'api' / 'json' / 'reference_data'/ 'teams_numbers_by_year.json'
START_YEAR = 2026
END_YEAR = 2010


with open(DISTRICT_REFERENCE_FILE) as district_reference_file:
    district_reference_dict = json.load(district_reference_file)
for loop_year in range(START_YEAR,END_YEAR-1,-1):
    district_key_list = district_reference_dict[str(loop_year)]
    for district_key in district_key_list:
        tba_team_api_url = build_tba_teams_from_district_key_url(district_key)
        pull_and_save_tba_api_data(tba_team_api_url)





teams_numbers_dict_by_year_set_dict = defaultdict(set)
team_files = [p.name for p in Path(TEAMS_FOLDER).iterdir() if p.is_file()]
for file_name in team_files:
    folder_and_file_path = TEAMS_FOLDER / file_name
    file_name_split = file_name.split('|')
    loop_year = file_name_split[2][:4]
    with open(folder_and_file_path) as file:
        json_data = json.load(file)

    team_number_list = []
    for i in range(len(json_data)):
        curr_dict = json_data[i]
        team_number = curr_dict["team_number"]
        team_number_list.append(team_number)
    teams_numbers_dict_by_year_set_dict[loop_year].update(team_number_list)

teams_numbers_dict_by_year_list_dict = {}
for key in teams_numbers_dict_by_year_set_dict:
    values = teams_numbers_dict_by_year_set_dict[key]
    values_list = list(values)
    values_list_ordered = sorted(values_list)
    teams_numbers_dict_by_year_list_dict[key] = values_list_ordered

with open(SAVE_PATH, 'w') as save_file:
    json.dump(teams_numbers_dict_by_year_list_dict, save_file, indent = 2)