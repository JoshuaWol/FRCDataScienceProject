from api.frc_and_tba_api_url_builders import *
from api.pull_and_save_api_url_data import *
import time


for year in range(2026,2014,-1):
    print(f"made it to {year} so far")
    frc_seasons_api_url = build_frc_seasons_url(year)
    pull_and_save_frc_api_data(frc_seasons_api_url)

    frc_districts_api_url = build_frc_districts_url(year)
    pull_and_save_frc_api_data(frc_districts_api_url)

    if year >= 2020:
        frc_events_api_url = build_frc_events_url(year)
    else:
        frc_events_api_url = build_frc_events_url_v2(year)
    pull_and_save_frc_api_data(frc_events_api_url)

    response_bool = True
    page = 1
    while response_bool: 
        frc_teams_api_url = build_frc_teams_url(year,page)
        response_bool = pull_and_save_teams_frc_api_data(frc_teams_api_url)
        page += 1
        print(year, page)

    time.sleep(0.5)
 