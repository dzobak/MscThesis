import pandas as pd
from utils import *
# _____________________________Relabeling________________________________


def get_scope_at_level(scope, lvl, sep='/'):
    split = tuple(scope.rsplit(sep))
    return split[min(len(split)-1, lvl)]


def relabel_function(df: pd.DataFrame, column: str, **kwargs):
    print('Scope examples: ')
    for i in range(5):
        print(df[kwargs['scope_column']][i*5 % len(df)])
    sc_lvl = int(input('Select the scope level: '))
    df[column] = df[kwargs['scope_column']].apply(
        get_scope_at_level, lvl=sc_lvl)
    return df


def execute_relabel(log, **kwargs):

    if kwargs['is_event_transformation']:
        df = relabel_function(log.events, column='ocel:activity', **kwargs)
        log.events = df
    elif kwargs['is_object_transformation']:
        df = log.objects[log.objects[log.object_id_column]
                         == kwargs['object_type']].copy()
        df = relabel_function(df, column=log.object_id_column, **kwargs)
        log.objects = df

    return log
