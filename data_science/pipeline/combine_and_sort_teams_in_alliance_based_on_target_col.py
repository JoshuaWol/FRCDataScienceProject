import pandas as pd


def combine_and_sort_teams_in_alliance_based_on_target_col_and_match_key(df_original:pd.DataFrame, target_col:str, *, index:list = ['match_key','alliance','auto_won', 'actual_time','auto_points'],
                                                                          non_stats_cols:list = ['team_key', 'match_key', 'actual_time', 'auto_points', 'alliance', 'opp_auto_points','rank', 'auto_won'] ) -> pd.DataFrame:
    #import best parameters from optuna study and sql data
    df = df_original.copy()
    num_cols = df.select_dtypes(include = 'number').columns
    df[num_cols] = df[num_cols].fillna(0)
    df = df.sort_values(target_col, ascending= False)
    df['rank'] = df.groupby(['match_key','alliance']).cumcount() + 1
    df['rank'] = "team_key" + df['rank'].astype(str)

    wide_df = df.pivot(index = index, columns = 'rank', values = 'team_key')
    df = df.drop(columns='rank')


    stat_cols = [col for col in df.columns
                if col not in non_stats_cols ]


    for i, col in enumerate(['team_key1', 'team_key2', 'team_key3'],1):
        rename_dict = {col: f't{i}_{col}' for col in stat_cols}
        wide_df = wide_df.merge(
            df.set_index(['team_key']+ index)[stat_cols],
            left_on = [col] + index,
            right_index = True,
            how = 'left'
        ).rename(columns = rename_dict)
    wide_df = wide_df.reset_index()
    return wide_df