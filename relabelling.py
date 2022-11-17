import pandas as pd
from functions import *
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

    if kwargs['evt_or_obj'] == 'e':
        df = relabel_function(log.events, column='ocel:activity', **kwargs)
        log.events = df
    elif kwargs['evt_or_obj'] == 'o':
        df = log.objects[log.objects[kwargs['object_column']]
                         == kwargs['object_type']]
        df = relabel_function(df, column=kwargs['object_column'], **kwargs)
        log.objects = df

    return log
