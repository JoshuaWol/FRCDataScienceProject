def get_folder_from_frc_api_url(inputURL: str) -> str:
    from pathlib import Path 
    import re  

    url_after_v3_slash = re.split('.0/',inputURL)
    url_after_v3_slash_split_list = re.split(r"[/?]",url_after_v3_slash[1])
    ROOT = next(p for p in Path(__file__).resolve().parents if (p/".git").exists())    
    if len(url_after_v3_slash_split_list) < 2:
        callFolder = 'seasons_data'
    else:
        callFolder = url_after_v3_slash_split_list[1] + '_data'
    finalFolders = ROOT/ "api" / "json" / callFolder
    return finalFolders

def get_json_file_name_from_frc_api_url(inputURL: str) -> str:
    import re
    url_after_v3_slash = re.split('.0/',inputURL)
    file_name_for_save = url_after_v3_slash[1].replace('/','|') + ".json"
    return file_name_for_save

def get_folder_and_json_file_name_from_frc_api_url(inputURL:str) -> str:
    folder_name = get_folder_from_frc_api_url (inputURL)
    file_name =  get_json_file_name_from_frc_api_url(inputURL)
    folder_and_file_name = folder_name / file_name
    return folder_and_file_name


def get_folder_from_tba_api_url(inputURL: str) -> str:
    from pathlib import Path 
    import re  
    folder_names_list = ['districts', 'events', 'matches', 'teams', 'seasons']

    url_after_v3_slash = re.split('i/v3/',inputURL)
    url_after_v3_slash_split_list = re.split(r"[/?]",url_after_v3_slash[1])
    ROOT = next(p for p in Path(__file__).resolve().parents if (p/".git").exists())    
    for i in range(len(url_after_v3_slash_split_list)-1,-1,-1):
        current_value = url_after_v3_slash_split_list[i]
        if current_value in folder_names_list:
            call_folder = current_value + "_data"
            exit
    if call_folder:
        finalFolders = ROOT/ "api" / "json" / call_folder
        return finalFolders
    else:
        print("call_folder could not be found for the url given")

def get_json_file_name_from_tba_api_url(inputURL: str) -> str:
    import re
    url_after_v3_slash = re.split('i/v3/',inputURL)
    file_name_for_save = url_after_v3_slash[1].replace('/','|') + ".json"
    return file_name_for_save

def get_folder_and_json_file_name_from_tba_api_url(inputURL:str) -> str:
    folder_name = get_folder_from_tba_api_url (inputURL)
    file_name =  get_json_file_name_from_tba_api_url(inputURL)
    folder_and_file_name = folder_name / file_name
    return folder_and_file_name