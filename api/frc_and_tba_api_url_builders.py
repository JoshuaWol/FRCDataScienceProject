BASE_FRC_URL = "https://frc-api.firstinspires.org/v3.0/" 
BASE_URL_FRC_V2 = "https://frc-api.firstinspires.org/v2.0/" 
BASE_THE_BLUE_ALLIANCE_URL = "https://www.thebluealliance.com/api/v3/"


## The Blue Alliance API Call Bundle
def build_tba_districts_url(year:int|str) -> str:
    return BASE_THE_BLUE_ALLIANCE_URL + "districts/" +str(year)


def build_tba_events_url(year:int|str) -> str:
    return BASE_THE_BLUE_ALLIANCE_URL + "events/" + str(year)


def build_tba_teams_from_district_key_url(district_key:str) -> str:
    return BASE_THE_BLUE_ALLIANCE_URL + "/district/" + district_key + "/teams"


def build_tba_teams_from_page_number_url(page_number:str|int) -> str:
    return BASE_THE_BLUE_ALLIANCE_URL + "/teams/" + str(page_number)


def build_tba_matches_from_event_key_url(event_key:str) -> str:
    return BASE_THE_BLUE_ALLIANCE_URL + '/event/' + event_key + "/matches"



##FRC API Call Bundle
def build_frc_seasons_url(year:int|str) -> str:
    return BASE_FRC_URL + str(year)


def build_frc_districts_url(year:int|str,) -> str:
    return BASE_FRC_URL + str(year) + '/districts'


def build_frc_events_url(year:int|str) -> str:
    return BASE_FRC_URL + str(year) + '/events'


def build_frc_events_url_v2(year:int|str) -> str:
    return BASE_URL_FRC_V2 + str(year) + '/events'


def build_frc_teams_url(year:int|str, page:int = 1) -> str:
    return BASE_FRC_URL + str(year) + '/teams' + f"?page={page}"


def build_frc_scores_url(year:int|str, event_code:str, tournament_level:int) -> str:
     tournament_level_list = ["None", "Practice", "Qualification", "Playoff"]
     tournament_level_str = tournament_level_list[tournament_level-1]
     return   BASE_FRC_URL + str(year) + '/scores' + f"/{event_code}" + f"/{tournament_level_str}"


def build_frc_matches_url(year:int|str, event_code:str, tournament_level:int) -> str:
     tournament_level_list = ["None", "Practice", "Qualification", "Playoff"]
     tournament_level_str = tournament_level_list[tournament_level-1]
     return   BASE_FRC_URL + str(year) + '/matches' + f"/{event_code}" + f"/{tournament_level_str}"   
