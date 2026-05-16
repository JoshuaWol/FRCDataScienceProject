import numpy as np


LOOKBACK_RANGE = [3,5,10, 'season']
MATCH_FUNCTIONS = ['mean', 'max', 'min', 'std', 'trend']

def get_math_list() -> list:
    col_math_list = ['team_key','match_key', 'actual_time','last_auto_points']
    for i in LOOKBACK_RANGE:
        for each in MATCH_FUNCTIONS:
            col_math_list.append(f"{each}_{i}_last_auto_points")
    col_math_list.append("prev_match_count")
    return col_math_list


def get_math_calced_list(scores:list[int]) -> list[int]:
    count = len(scores)-1
    result_list = []
    if count == 0:
        result_list.append([0 for i in range(len(get_math_list())-3)])
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
    return result_list