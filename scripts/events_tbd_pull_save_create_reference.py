import json
from pathlib import Path
import subprocess


from api.frc_and_tba_api_url_builders import *
from api.pull_and_save_api_url_data import *


REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
EVENTS_FOLDER = REPO_ROOT / 'api' / 'json' / 'events_data'
SAVE_PATH = REPO_ROOT / 'api' / 'json' / 'reference_data'/ 'event_keys_by_year.json'
START_YEAR = 2026
END_YEAR = 2010


for loop_year in range(START_YEAR,END_YEAR-1,-1):
    tba_event_api_url = build_tba_events_url(loop_year)
    pull_and_save_tba_api_data(tba_event_api_url)





events_key_dict_by_year = {}
for loop_year in range(START_YEAR,END_YEAR-1,-1):
    file_name = f"events|{loop_year}.json"
    folder_and_file_path = EVENTS_FOLDER / file_name 
    with open(folder_and_file_path) as file:
        json_data = json.load(file)

    event_keys = []
    for i in range(len(json_data)):
        curr_dict = json_data[i]
        event_keys.append(curr_dict["key"])
    events_key_dict_by_year[loop_year] = event_keys
with open(SAVE_PATH, 'w') as save_file:
    json.dump(events_key_dict_by_year, save_file, indent = 2)