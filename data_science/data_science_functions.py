import pandas as pd
import numpy as np


def transform_shift_to_phase(df:pd.DataFrame) -> pd.DataFrame:
    df['phase1_points'] = np.where(df['auto_won'] == 0, df['shift1_points'], df['shift2_points'])
    df['phase2_points'] = np.where(df['auto_won'] == 0, df['shift3_points'], df['shift4_points'])
    df.drop(columns = ['shift1_points', 'shift2_points', 'shift3_points', 'shift4_points'], inplace= True)
    return df