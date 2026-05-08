def pull_and_save_frc_api_data(frc_api_url:str, debug:bool = False) -> None:
    from pathlib import Path
    import json
    import requests

    from api.get_folder_file_both_from_api_url import get_folder_and_json_file_name_from_frc_api_url
    from api.get_credentials import get_frc_credentials
    
    headers_auth = {"Authorization": f"Basic {get_frc_credentials()}"}


    FolderAndFileName = get_folder_and_json_file_name_from_frc_api_url(frc_api_url)

    if Path(FolderAndFileName).is_file():
        print(f'skipped {FolderAndFileName} because the file already exists')
    
    else:
        response = requests.get(frc_api_url, headers=headers_auth)
        response_json = response.json()
        if debug:
            print(response)
        if not response.ok:
            print("Error: " + str(response.status_code) + " - " + response.reason)
        else:
            with open(FolderAndFileName, "w") as f:
                json.dump(response_json, f, indent=2)


def pull_and_save_teams_frc_api_data(frc_api_url:str, debug:bool = False) -> None:
    from pathlib import Path
    import json
    import requests

    from api.get_folder_file_both_from_api_url import get_folder_and_json_file_name_from_frc_api_url
    from api.get_credentials import get_frc_credentials
    
    headers_auth = {"Authorization": f"Basic {get_frc_credentials()}"}

    FolderAndFileName = get_folder_and_json_file_name_from_frc_api_url(frc_api_url)
    response_skip = False
    if Path(FolderAndFileName).is_file():
        print(f'skipped {FolderAndFileName} because the file already exists')
        response_skip = True
    else:
        response = requests.get(frc_api_url, headers=headers_auth)
        if not response.ok:
            print("Error: " + str(response.status_code) + " - " + response.reason)
        else:
            response_json = response.json()
            if len(response.json()['teams'])>0:
                with open(FolderAndFileName, "w") as f:
                    json.dump(response_json, f, indent=2)
    if debug:
        print(response.ok, response_skip, response_json['teams'])
    if response_skip:
        return True
    elif (response.ok & len(response_json['teams'])>0):
        return True
    else:
        return False


def pull_and_save_tba_api_data(tba_api_url:str, debug:bool = False) -> None:
    from pathlib import Path
    import json
    import requests

    from api.get_folder_file_both_from_api_url import get_folder_and_json_file_name_from_tba_api_url
    from api.get_credentials import get_tba_credentials
    
    headers_auth = {"X-TBA-Auth-Key": get_tba_credentials()}


    FolderAndFileName = get_folder_and_json_file_name_from_tba_api_url(tba_api_url)

    if Path(FolderAndFileName).is_file():
        print(f'skipped {FolderAndFileName} because the file already exists')
    
    else:
        response = requests.get(tba_api_url, headers=headers_auth)
        response_json = response.json()
        if debug:
            print(response)
        if not response.ok:
            print("Error: " + str(response.status_code) + " - " + response.reason)
        else:
            with open(FolderAndFileName, "w") as f:
                json.dump(response_json, f, indent=2)


def pull_and_save_tba_api_data_if_exists(tba_api_url:str, debug:bool = False) -> bool:
    from pathlib import Path
    import json
    import requests

    from api.get_folder_file_both_from_api_url import get_folder_and_json_file_name_from_tba_api_url
    from api.get_credentials import get_tba_credentials
    
    headers_auth = {"X-TBA-Auth-Key": get_tba_credentials()}


    FolderAndFileName = get_folder_and_json_file_name_from_tba_api_url(tba_api_url)

    if Path(FolderAndFileName).is_file():
        print(f'skipped {FolderAndFileName} because the file already exists')
        return True
    else:
        response = requests.get(tba_api_url, headers=headers_auth)
        response_json = response.json()
        if debug:
            print(response)
        if not response.ok:
            print("Error: " + str(response.status_code) + " - " + response.reason)
        elif len(response_json)>0:
            with open(FolderAndFileName, "w") as f:
                json.dump(response_json, f, indent=2)
            return True
        return False