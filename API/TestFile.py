import numpy as np
import http
import pandas as pd
import json
import sys
import os
import requests
from dotenv import load_dotenv
import base64
from pathlib import Path
load_dotenv()

# FIRST_API_URL = "https://frc-api.firstinspires.org/v3.0/2019"
# FIRST_API_URL = "https://frc-api.firstinspires.org/v3.0/2026/events?eventCode=&teamNumber=488&districtCode=pnw&excludeDistrict=&weekNumber&tournamentType"

FIRST_API_AUTH_KEY = os.getenv("FIRST_API_AUTH_KEY")
FIRST_API_USERNAME = os.getenv("FIRST_API_USERNAME")
FIRST_API_ACCESS_TOKEN = FIRST_API_USERNAME + ":" + FIRST_API_AUTH_KEY
credentials = base64.b64encode(FIRST_API_ACCESS_TOKEN.encode()).decode()

headers = {"Authorization": f"Basic {credentials}"}


FIRST_API_URL = "https://frc-api.firstinspires.org/v3.0/2014/scores/WASNO/Qualification"
response = requests.get(FIRST_API_URL, headers=headers)


# print(response_json['Events'][0])
if not response.ok:
    print("Error: " + str(response.status_code) + " - " + response.reason)
# else:
#     response_json = response.json()
#     # print(response_json)

#     for i in range(len(response_json['MatchScores'])):
#         print(f'_____Match {i}_____')
#         for each in response_json['MatchScores'][i].keys():
#             print(each + " : " + str(response_json['MatchScores'][i][each]))
else:
    ROOT = next(p for p in Path(__file__).resolve().parents if (p/".git").exists())
    Folders = ROOT / "API" / "JSON"
    response_json = response.json()
    URLSplit = FIRST_API_URL.split('v3.0')
    FileSave = URLSplit[1].replace('/','|')
    with open(Folders / FileSave +".json", "w") as f:
        json.dump(response_json, f, indent=2)
        