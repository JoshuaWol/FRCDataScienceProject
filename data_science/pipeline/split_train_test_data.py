import pandas as pd

def split_train_test_data_from_target_column_feature_columns_and_date(df:pd.DataFrame,*, target_col:str, feature_cols:list[str], date:str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    X = df[feature_cols]
    Y = df[target_col]

    train_mask = df['actual_time'] < date
    test_mask = df['actual_time'] >= date

    X_train = X[train_mask]
    Y_train = Y[train_mask]
    X_test = X[test_mask]
    Y_test = Y[test_mask]
    return X_train, X_test, Y_train, Y_test

