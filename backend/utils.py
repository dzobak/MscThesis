from typing import List
import pandas as pd
import os
from OCEL_extended import OCEL_ext
import numpy as np


def get_scope_tuple(scope: str, sep='/') -> tuple:
    scope_tup = tuple(scope.rsplit(sep)) if type(scope) == str else tuple()
    return scope_tup


def get_max_scope_depth(series: pd.Series):
    tuple_series = series.apply(get_scope_tuple)
    return max([len(x) for x in tuple_series])


def concat_dicts(iterable) -> dict:
    new_dict = {}
    for dict in iterable:
        new_dict.update(dict)
    return new_dict


def show_scope_examples(df: pd.DataFrame, scope_column: str, amount_examples=5) -> None:
    print('Scope examples: ')
    if amount_examples < len(df):
        for i in range(amount_examples):
            print(df[scope_column][i*13 % (len(df)-1)])
    else:
        for scope in df[scope_column]:
            print(scope)


def keep_n_levels(scope_str: str, n: int, left_side=True) -> str:
    scope_tuple = get_scope_tuple(scope_str)
    n = min(len(scope_tuple), n)
    if left_side:
        truncated_scope = '/'.join(scope_tuple[:n])
    else:
        truncated_scope = '/'.join(scope_tuple[-n:])
    return truncated_scope

def remove_n_levels(scope_str: str, n: int, left_side=True) -> str:
    scope_tuple = get_scope_tuple(scope_str)
    n = min(len(scope_tuple), n)
    if left_side:
        truncated_scope = '/'.join(scope_tuple[n:])
    else:
        truncated_scope = '/'.join(scope_tuple[:-n])
    return truncated_scope


def get_file_folder() -> str:
    return os.path.join('event_log_files', '')


def get_filepath_from_name(name: str) -> str:
    return os.path.join('.', 'event_log_files', name+'.jsonocel')


def get_name_from_filepath(path: str, filetype='jsonocel') -> str:
    folder = get_file_folder()
    name = path.split(folder)[1]
    name = name.split('.'+filetype)[0]
    return name


def get_column_functions_by_dtype(dtype: type) -> List[str]:
    if dtype == type(''):
        return ['MODE', 'CONCAT', 'MAX', 'MIN', 'DISCARD']
    #TODO: Nan values can by identified as number even if the rest of the column is string
    elif dtype == type(0) or dtype == type(1.0) or np.issubdtype(dtype, np.number):
        return ['SUM','MAX', 'MIN', 'COUNT', 'AVG', 'MEDIAN', 'MODE', 'DISCARD']
    print(dtype)
    return ["good job"]


def get_column_function_options(log: OCEL_ext, **kwargs) -> dict:
    col_functions = {}
    if kwargs['is_event_transformation']:
        df = log.events
        col_functions[log.event_id_column] = ['MIN', 'MAX', 'MODE']
        col_functions[log.event_timestamp] = ['MIN and MAX', 'MIN', 'MAX']
        col_functions[log.event_activity] = ['TRUNCATE'] if log.event_activity in log.event_scope_columns\
            else ['GROUP BY']

        for scope in log.event_scope_columns:
            if scope not in col_functions:
                col_functions[scope] = ['TRUNCATE', 'MODE', 'COUNT', 'DISCARD']

    elif kwargs['is_object_transformation']:
        df = log.objects
        col_functions[log.object_id_column] = ['MIN', 'MAX', 'MODE']
        col_functions[log.object_type_column] = ['GROUP BY']

        for scope in log.object_scope_columns:
            if scope not in col_functions:
                col_functions[scope] = ['TRUNCATE', 'GROUP BY', 'DISCARD']

    for column in df.columns:
        if column not in col_functions:
            print(df[column].dtypes)
            col_functions[column] = get_column_functions_by_dtype(
                type(df.iloc[df[column].first_valid_index()][column]))
    return col_functions

def rename_file(old_name:str, new_name:str)->None:
    os.rename(get_filepath_from_name(old_name), get_filepath_from_name(new_name))

def delete_file(name:str)->None:
    os.remove(get_filepath_from_name(name))

