import json
import requests


from api.get_credentials import get_frc_credentials
from api.frc_api_url_builders import *
from api.pull_and_save_api_url_data import *

for for_year in range(2026,2009,-1):
    tba_district_api_url = build_tba_districts_url(for_year)
    pull_and_save_tba_api_data(tba_district_api_url)