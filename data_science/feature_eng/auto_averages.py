from collections import defaultdict
import pandas as pd
import time


from sql.load_db_to_df import load_df_from_db
from data_science.data_science_functions import transform_shift_to_phase
from config import IMPORTANT_FEATURES
from function_for_feature_eng import get_math_list, get_math_calced_list
from sql.data_science_db import get_sqlalchemy_connection

start_time = time.time()
match_data_df = load_df_from_db('features', 'matches_eda')
match_data_df.sort_values(ascending = True, by = 'actual_time', inplace= True)
match_data_df = transform_shift_to_phase(match_data_df[IMPORTANT_FEATURES])
match_data_df_non_num = match_data_df.drop( labels  = match_data_df.select_dtypes(include = 'number').columns.tolist(), axis = 1)
calc_df = match_data_df[['actual_time','team_key1','team_key2','team_key3','auto_points','match_key']]
team_col_name = ['team_key1','team_key2','team_key3']

calc_df = calc_df.melt(id_vars = calc_df.columns.difference(team_col_name).tolist(), value_vars = team_col_name, var_name = "droppable", value_name = "team_key")
calc_df.drop(columns = 'droppable', inplace = True)
calc_df.sort_values(ascending = True, by = ['team_key','actual_time'], inplace=True)
calc_df.reset_index(inplace = True)


prev_team = ""
team_auto_dict = defaultdict(list)
col_list=get_math_list()
calced_auto_data = []
team_seen = defaultdict(list)
for row in range(0,len(calc_df)):
    
    current_row = calc_df.iloc[[row]]
    current_team = current_row['team_key'].item()
    current_match = current_row['match_key'].item()
    current_time = current_row['actual_time'].item()
    calced_list = [current_team, current_match, current_time]
    team_seen[current_match].append(current_team)
    team_auto_dict[current_team].append(current_row['auto_points'].item())
    dict_list = team_auto_dict[current_team]
    if len(dict_list) > 1 :
        calced_list.extend(get_math_calced_list(dict_list))
        calced_auto_data.append(calced_list)
    prev_team = current_team


calced_auto_df = pd.DataFrame(calced_auto_data, columns = col_list)



with get_sqlalchemy_connection() as conn:
    calced_auto_df.to_sql(name = 'match_auto_data_calc',  con = conn, schema = 'features', if_exists='append', index=False)


end_time = time.time()
print(start_time - end_time)


