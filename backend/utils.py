import pandas as pd
import os


def get_scope_tuple(scope: str, sep='/') -> tuple:
    scope_tup = tuple(scope.rsplit(sep)) if type(scope) == str else tuple()
    return scope_tup


def get_max_scope_depth(series: pd.Series):
    tuple_series = series.apply(get_scope_tuple)
    return max([len(x) for x in tuple_series])


def concat_dicts(series) -> dict:
    new_dict = {}
    for dict in series:
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
        truncated_scope = '/'.join(scope_tuple[:n+1])
    else:
        truncated_scope = '/'.join(scope_tuple[-n:])
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
