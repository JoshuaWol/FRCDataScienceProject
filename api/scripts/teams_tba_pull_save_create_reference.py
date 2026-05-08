from collections import defaultdict

import json
from pathlib import Path


from api.frc_and_tba_api_url_builders import build_tba_teams_from_page_number_url
from api.pull_and_save_api_url_data import pull_and_save_tba_api_data_if_exists
from config import REPO_ROOT


TEAMS_FOLDER = REPO_ROOT / 'api' / 'json' / 'teams_data'
SAVE_PATH = REPO_ROOT / 'api' / 'json' / 'reference_data'/ 'team_numbers.json'


loop_run = True
page = 0
while loop_run:
    loop_url = build_tba_teams_from_page_number_url(page)
    loop_run = pull_and_save_tba_api_data_if_exists(loop_url)
    page += 1
print(loop_run)


teams_numbers_dict_by_year_set_dict = defaultdict(set)
team_paths= [p for p in Path(TEAMS_FOLDER).iterdir() if p.is_file()]
set_team_keys = set()
team_keys = []
for file_path in team_paths:
    with open(file_path) as file:
        loop_team_json_data = json.load(file)
    for team_data in loop_team_json_data:
        team_key = team_data['key']
        if team_key not in set_team_keys:
            team_keys.append(team_key)
            set_team_keys.add(team_key)

teams_keys = sorted(team_keys)

with open(SAVE_PATH, 'w') as save_file:
    json.dump(teams_keys, save_file, indent = 2)