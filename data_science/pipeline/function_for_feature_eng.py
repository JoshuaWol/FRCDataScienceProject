import numpy as np


LOOKBACK_RANGE = [3,5,10, 'season']
MATCH_FUNCTIONS = ['mean', 'max', 'min', 'std', 'trend']

def get_match_auto_data_list() -> list:
    col_math_list = ['team_key','match_key', 'actual_time', 'last_auto_points']
    for i in LOOKBACK_RANGE:
        for each in MATCH_FUNCTIONS:
            col_math_list.append(f"{each}_{i}_last_auto_points")
    col_math_list.append("prev_match_count")
    col_math_list.extend(['auto_points', 'alliance', 'opp_auto_points'])
    return col_math_list


def get_math_list_first_match_missing() -> list:
    col_math_list = ['last_auto_points']
    for i in LOOKBACK_RANGE:
        for each in MATCH_FUNCTIONS:
            col_math_list.append(f"{each}_{i}_last_auto_points")
    return col_math_list

def get_match_auto_data_value_list(scores:list[int],alliance:str, opp_score) -> list[int]:
    count = len(scores)-1
    result_list = []
    if count == 0:
        result_list.extend([None for i in range(len(get_match_auto_data_list())-7)])
        result_list.append(0)
        result_list.extend([scores[-1],alliance,opp_score])
        return result_list
    result_list.append(scores[-2])
    for i_track in LOOKBACK_RANGE:
        i=i_track
        if i == 'season':
            i = np.inf
        if i > count:
            i = count
        for each in MATCH_FUNCTIONS[:len(MATCH_FUNCTIONS)-1]:
            func = getattr(np, each)
            result = func(scores[-i:])
            result_list.append(result)
        if i < 3:
            slope = 0
        else:
            slope,intercept = np.polyfit(range(i),scores[:i], deg = 1)
        result_list.append(slope)
    result_list.append(count)
    result_list.extend([scores[-1],alliance, opp_score])
    return result_list