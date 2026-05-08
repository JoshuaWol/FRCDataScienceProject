# ruff: noqa

from api.get_credentials import get_frc_credentials
from api.frc_and_tba_api_url_builders import * #no qa
from api.pull_and_save_api_url_data import  pull_and_save_tba_api_data

headers = {"Authorization": f"Basic {get_frc_credentials()}"}

tba_district_api_url = build_tba_teams_from_page_number_url(7)
# response = requests.get('https://frc-api.firstinspires.org/v2.0/2018/events', headers=headers)
# print(response.ok,response.status_code,response.content)
print(tba_district_api_url)
pull_and_save_tba_api_data(tba_district_api_url, True)
