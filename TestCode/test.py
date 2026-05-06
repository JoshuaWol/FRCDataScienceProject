import json
import requests


from api.get_credentials import get_frc_credentials
from api.frc_and_tba_api_url_builders import *
from api.pull_and_save_api_url_data import *

headers = {"Authorization": f"Basic {get_frc_credentials()}"}

tba_district_api_url = build_tba_districts_url(2016)
# response = requests.get('https://frc-api.firstinspires.org/v2.0/2018/events', headers=headers)
# print(response.ok,response.status_code,response.content)
print(tba_district_api_url)
pull_and_save_tba_api_data(tba_district_api_url, True)
