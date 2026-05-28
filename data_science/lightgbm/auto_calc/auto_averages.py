from collections import defaultdict
import pandas as pd
import time
import numpy as np


from sql.load_db_to_df import load_df_from_db
from data_science.pipeline.transform_shift_to_phase import transform_shift_to_phase
from config import IMPORTANT_FEATURES
from function_for_feature_eng import get_match_auto_data_list, get_match_auto_data_value_list, get_math_list_first_match_missing
from sql.data_science_db import get_sqlalchemy_connection

start_time = time.time()
match_data_df = load_df_from_db('features', 'matches_eda')
match_data_df.sort_values(ascending = True, by = 'actual_time', inplace= True)
match_data_df = transform_shift_to_phase(match_data_df[IMPORTANT_FEATURES])
match_data_df_non_num = match_data_df.drop( labels  = match_data_df.select_dtypes(include = 'number').columns.tolist(), axis = 1)
calc_df = match_data_df[['actual_time','team_key1','team_key2','team_key3','auto_points','match_key','alliance']]
calc_df['opp_auto_points'] = calc_df.groupby('match_key')['auto_points'].transform('sum') - calc_df['auto_points']
team_col_name = ['team_key1','team_key2','team_key3']
calc_df.head(25)

calc_df = calc_df.melt(id_vars = calc_df.columns.difference(team_col_name).tolist(), value_vars = team_col_name, var_name = "droppable", value_name = "team_key")
calc_df.drop(columns = 'droppable', inplace = True)
calc_df.sort_values(ascending = True, by = ['team_key','actual_time'], inplace=True)
calc_df.reset_index(inplace = True)


prev_team = ""
team_auto_dict = defaultdict(list)
col_list=get_match_auto_data_list()
calced_auto_data = []
team_seen = defaultdict(list)
for row in range(0,len(calc_df)):
    
    current_row = calc_df.iloc[[row]]
    current_team = current_row['team_key'].item()
    current_match = current_row['match_key'].item()
    current_time = current_row['actual_time'].item()
    current_alliance = current_row['alliance'].item()
    current_opp_score = current_row['opp_auto_points'].item()
    calced_list = [current_team, current_match, current_time]
    team_seen[current_match].append(current_team)
    team_auto_dict[current_team].append(current_row['auto_points'].item())
    dict_list = team_auto_dict[current_team]
    calced_list.extend(get_match_auto_data_value_list(dict_list, current_alliance, current_opp_score))
    calced_auto_data.append(calced_list)
    prev_team = current_team


calced_auto_df = pd.DataFrame(calced_auto_data, columns = col_list)
calced_auto_df.sort_values(by = 'actual_time', ascending= True, inplace=True)
calced_auto_df.reset_index(drop=True, inplace = True)

print(calced_auto_df.head())
end_time = time.time()
print(start_time - end_time)


for row in range(len(calced_auto_df)):
    last_row = row-1
    if pd.isna(calced_auto_df.at[row,'last_auto_points']) :
        if row == 0 or row == 1:
            print('check')
            for each in get_math_list_first_match_missing():
                calced_auto_df.at[row,each] = 0
            continue
        if calced_auto_df.at[row,'match_key'] == calced_auto_df.at[row-1,'match_key']:
            last_row -= 1
        for each in get_math_list_first_match_missing():
            med = calced_auto_df.loc[:last_row, each].median()
            calced_auto_df.at[row, each] = 0 if pd.isna(med) else med


print(calced_auto_df.head())
end_time = time.time()
print(start_time - end_time)

with get_sqlalchemy_connection() as conn:
    calced_auto_df.to_sql(name = 'match_auto_data_calc',  con = conn, schema = 'features', if_exists='append', index=False)


end_time = time.time()
print(start_time - end_time)


