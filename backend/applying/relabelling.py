import pandas as pd
from utils import *
from enum import Enum


class Variant(Enum):
    KEEP_LEFT = 'l'
    KEEP_RIGHT = 'r'
    KEEP_INDEX = 'i'


def get_scope_by_index(scope: str, indexes: list[int], sep='/'):
    split = tuple(scope.rsplit(sep))
    indexes.sort()
    sel_levels = []
    for i in indexes:
        if i < len(split)-1 and i >= 0:
            sel_levels.append(split[i])
        elif i >= len(split)-1:
            sel_levels.append(split[i])
    # sel_levels = [min(i,len(split)-1)for i in indexes]
    return sep.join(sel_levels)


def relabel_function(df: pd.DataFrame, column: str, **kwargs):
    # sc_indexes = list(map(int, input('Select the scope level: ').split(',')))
    if kwargs['Variant'] == Variant.KEEP_INDEX.value:
        df[column] = df[kwargs['scope_column']].apply(
            get_scope_by_index, indexes=kwargs['sc_indexes'])
    elif kwargs['Variant'] == Variant.KEEP_LEFT.value:
        df[column] = df[kwargs['scope_column']].apply(
            keep_n_levels, n=kwargs['n'])
    elif kwargs['Variant'] == Variant.KEEP_RIGHT.value:
        df[column] = df[kwargs['scope_column']].apply(
            keep_n_levels, n=kwargs['n'], left_side=False)
    return df


def execute_relabelling(log, **kwargs):
    df = log.events if kwargs['is_event_transformation'] else log.objects
    # show_scope_examples(df, kwargs['scope_column'])
    # print('Possible variants for subscope are: Keep left(l), Keep right(r), Index(i)')
    # kwargs['Variant'] = input(str('Specify the variant for subscope: '))
    # if kwargs['Variant'] == Variant.KEEP_LEFT.value or kwargs['Variant'] == Variant.KEEP_RIGHT.value:
    #     kwargs['n'] = int(input('Specify the amount of levels to be kept: '))
    # elif kwargs['Variant'] == Variant.KEEP_INDEX.value:
    #     kwargs['sc_indexes'] = list(map(int, input(
    #         'Provides the Index(es) of scope levels to be kept: ').split(',')))
    # else:
    #     raise Exception("No such Variant")
    kwargs['Variant'] = Variant.KEEP_LEFT.value
    kwargs['n'] = kwargs['levels'][0]
    if kwargs['is_event_transformation']:
        df = relabel_function(log.events, column='ocel:activity', **kwargs)
        log.events = df
    elif kwargs['is_object_transformation']:
        df = log.objects[log.objects[log.object_type_column]
                         == kwargs['object_type']].copy()
        df = relabel_function(df, column=log.object_type_column, **kwargs)
        log.objects = df
        print(log.objects)

    return log
