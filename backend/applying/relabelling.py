import pandas as pd
from utils import *
from enum import Enum
import re


class Variant(Enum):
    KEEP_LEFT = 'kl'
    KEEP_RIGHT = 'kr'
    KEEP_INDEX = 'ki'
    REMOVE_LEFT = 'rl'
    REMOVE_RIGHT = 'rr'
    REMOVE_INDEX = 'ri'


def get_scope_by_index(scope: str, indexes: list[int], sep='/'):
    split = tuple(scope.rsplit(sep))
    indexes.sort()
    sel_levels = []
    for i in indexes:
        if i < len(split)-1 and i >= 0:
            sel_levels.append(split[i])
        elif i >= len(split)-1:
            sel_levels.append(split[i])
            break
    # sel_levels = [min(i,len(split)-1)for i in indexes]
    return sep.join(sel_levels)

def remove_scope_by_index(scope: str, indexes: list[int], sep='/'):
    split = tuple(scope.rsplit(sep))
    sel_levels = []
    for i in len(split):
        if i not in indexes:
            sel_levels.append(split[i])
    return sep.join(sel_levels)

def relabel_function(df: pd.DataFrame, **kwargs):
    commands = parse_command(kwargs['relabel_command'])
    column = 'new_column' #kwargs['new_column']
    for kwargs in commands:
        # sc_indexes = list(map(int, input('Select the scope level: ').split(',')))
        if kwargs['Variant'] == Variant.KEEP_INDEX:
            modified_col = df[kwargs['scope_column']].apply(
                get_scope_by_index, indexes=kwargs['sc_indexes'])
        elif kwargs['Variant'] == Variant.KEEP_LEFT:
            modified_col = df[kwargs['scope_column']].apply(
                keep_n_levels, n=kwargs['n'])
        elif kwargs['Variant'] == Variant.KEEP_RIGHT:
            modified_col = df[kwargs['scope_column']].apply(
                keep_n_levels, n=kwargs['n'], left_side=False)
        elif kwargs['Variant'] == Variant.REMOVE_LEFT:
            modified_col = df[kwargs['scope_column']].apply(
                remove_n_levels, n=kwargs['n'])
        elif kwargs['Variant'] == Variant.REMOVE_RIGHT:
            modified_col = df[kwargs['scope_column']].apply(
                remove_n_levels, n=kwargs['n'], left_side=False)
        elif kwargs['Variant'] == Variant.KEEP_INDEX:
            modified_col = df[kwargs['scope_column']].apply(
                get_scope_by_index, indexes=kwargs['sc_indexes'])
        if column in df.columns:
            df[column] = [str(x) + '/' +str(y) for x, y in zip(df[column], modified_col)]
        else:
            df[column] = modified_col

    return df


def parse_command(rel_command: str):
    single_scope_commands = rel_command.split('CONCAT')
    commands = []
    for command in single_scope_commands:
        if len(command) > 2:
            kwargs = {}
            if re.search('KEEP', command):
                if re.search('LEFT', command):
                    kwargs['Variant'] = Variant.KEEP_LEFT
                elif re.search('RIGHT', command):
                    kwargs['Variant'] = Variant.KEEP_RIGHT
                elif re.search('INDEX', command):
                    kwargs['Variant'] = Variant.KEEP_INDEX
            elif re.search('REMOVE', command):
                if re.search('LEFT', command):
                    kwargs['Variant'] = Variant.REMOVE_LEFT
                elif re.search('RIGHT', command):
                    kwargs['Variant'] = Variant.REMOVE_RIGHT
                elif re.search('INDEX', command):
                    kwargs['Variant'] = Variant.REMOVE_INDEX
            print(command)
            scope_column = command.split('<')[1]
            scope_column = scope_column.split('>')[0]
            kwargs['scope_column'] = scope_column
            n = command.split('<')[2]
            n = n.split('>')[0]
            if re.search('INDEX', command):
                kwargs['sc_indexes'] = list(map(int, n.split(',')))
            else:
                kwargs['n'] = int(n)

            commands.append(kwargs)
    return commands


def execute_relabelling(log, **kwargs):
    # df = log.events if kwargs['is_event_transformation'] else log.objects
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
    # kwargs['Variant'] = Variant.KEEP_LEFT.value
    # kwargs['n'] = kwargs['levels'][0]
    if kwargs['is_event_transformation']:
        df = relabel_function(log.events, column='new:column', **kwargs)
        log.events = df
    elif kwargs['is_object_transformation']:
        df = log.objects[log.objects[log.object_type_column]
                         == kwargs['object_type']].copy()
        df = relabel_function(df, column='new:column', **kwargs)
        log.objects = df
        print(log.objects)

    return log
