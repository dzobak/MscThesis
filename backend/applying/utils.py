import pandas as pd


def get_scope_tuple(scope: str, sep='/') -> tuple:
    return tuple(scope.rsplit(sep))


def concat_dicts(series) -> dict:
    new_dict = {}
    for dict in series:
        new_dict.update(dict)
    return new_dict


def show_scope_examples(df: pd.DataFrame, scope_column: str,amount_examples=5) -> None:
    print('Scope examples: ')
    if amount_examples < len(df):
        for i in range(amount_examples):
            print(df[scope_column][i*13 % (len(df)-1)])
    else: 
        for scope in df[scope_column]:
            print(scope)

def keep_n_levels(scope_str:str, n:int, left_side=True)->str:
    scope_tuple = get_scope_tuple(scope_str)
    n = min(len(scope_tuple),n)
    if left_side:
        truncated_scope = '/'.join(scope_tuple[:n])
    else:
        truncated_scope = '/'.join(scope_tuple[-n:])
    return truncated_scope