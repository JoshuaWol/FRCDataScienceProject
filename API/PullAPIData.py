import json
import requests
import base64
from API.GetFolderFileBothFromAPI_URL import getFolderAndFileNameFromAPI_URL
from API.getCredentials import getCredentials


headers = {"Authorization": f"Basic {getCredentials()}"}


FIRST_API_URL = "https://frc-api.firstinspires.org/v3.0/2026/teams?page=1"
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

    response_json = response.json()
    FolderAndFileName = getFolderAndFileNameFromAPI_URL(FIRST_API_URL)
    with open(FolderAndFileName, "w") as f:
        json.dump(response_json, f, indent=2)


        