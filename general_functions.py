import pandas as pd
import numpy as np
from pathlib import Path
import os


def read_csv_in_folder(file_path):
    file_path = Path(file_path)
    list_of_files = list(i for i in os.listdir(file_path) if '.csv' in i)
    list_of_dfs = []
    for files in list_of_files:
        file = os.path.join(file_path, files)
        df = pd.read_csv(file)
        list_of_dfs.append(df)
    output = pd.concat(list_of_dfs)
    return output


def datetime_formatter(df, expected_interval):
    def datetime_datatype_changer(df1):
        if False in df1.index.str.contains('/', regex=False):
            df1.index = pd.to_datetime(df1.index, format='%Y-%m-%d %H:%M:%S')
        else:
            df1.index = pd.to_datetime(df1.index, format='mixed', dayfirst=True)

        print('Index\t\t\t\t\t', df1.index.dtype)
        print(df1.dtypes)
        df1.sort_index(inplace=True)
        print('First value\t\t\t\t', df1.index[0])
        print('First value\t\t\t\t', df1.index[-1])
        return df1

    def increasing_continuously(df1, interval):
        for facility in df1['Facility Code'].unique():
            print(facility)
            temp = df1.loc[df1['Facility Code'] == facility, :]
            datetime_df = temp.index.unique()
            time_intervals = datetime_df.to_series().diff()
            is_monotonic_increasing = time_intervals.iloc[1:].eq(time_intervals.iloc[1]).all()
            if is_monotonic_increasing:
                print("The DateTimeIndex is strictly increasing.")
            else:
                print("Missing values:")
                missing_values = datetime_df[time_intervals != expected_interval]
                print(missing_values)
                raise Exception('Some values are missing')
        return df1

    def remove_29_feb(df1):
        df1 = df1.loc[~((df1.index.month == 2) & (df1.index.day == 29))]
        return df1

    df = datetime_datatype_changer(df)
    check = input('Check increasing continuously?\tY for yes\tN for No')
    if check == 'N':
        pass
    elif check == 'Y':
        increasing_continuously(df, expected_interval)
    else:
        raise Exception('Wrong choice')
    leap_remove = input('Remove 29th Feb?\tY for yes\tN for No')
    if leap_remove == 'N':
        pass
    elif leap_remove == 'Y':
        remove_29_feb(df)
    else:
        raise Exception('Wrong choice')
    df.reset_index(inplace=True)
    return df


def general_formatter(df):
    def remove_trailing_white_spaces(df1):
        string_columns = df1.select_dtypes(include=['object']).columns
        df1[string_columns] = df1[string_columns].apply(lambda x: x.str.strip())
        return df1

    def nan_values(df1):
        nan_rows = df1.isna().any(axis=1)
        rows_with_nan = df1[nan_rows]
        if rows_with_nan.empty:
            print("The DataFrame does not contain NaN values.")
        else:
            print("The DataFrame contains NaN values.")
            print(rows_with_nan)
            nan_to_zero = input('Convert nan to 0:\tY for Yes\tN for No')
            if nan_to_zero == 'N':
                pass
            elif nan_to_zero == 'Y':
                df1 = df1.fillna(0)
            else:
                raise Exception('Wrong choice')
            print('Nan converted to 0')
        return df

    df = remove_trailing_white_spaces(df)
    df = nan_values(df)
    return df



