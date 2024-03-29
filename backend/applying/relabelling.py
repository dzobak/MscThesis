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


def remove_scope_by_index(scope: str, indexes: list[int], sep='/'):
    split = tuple(scope.rsplit(sep))
    sel_levels = []
    for i in len(split):
        if i not in indexes:
            sel_levels.append(split[i])
    return sep.join(sel_levels)

# def separate_column_name_and_rel_command()


def relabel_function(df: pd.DataFrame, **kwargs):
    rel_command = kwargs['relabel_command']
    if 'AS' in rel_command:
        new_column = rel_command.split('AS')[1]
        new_column = new_column.split('<')[1]
        kwargs['new_column'] = new_column.split('>')[0]
        rel_command = rel_command.split('AS')[0]
    else:
        kwargs['new_column'] = 'new:column'

    commands = parse_command(rel_command)
    print(commands)
    column = kwargs['new_column']
    new_column = pd.Series()
    for kwargs in commands:
        df_to_relabel = df[~df[kwargs['scope_column']].isna()]
        df_no_relabel = df[df[kwargs['scope_column']].isna()]
        # sc_indexes = list(map(int, input('Select the scope level: ').split(',')))
        if kwargs['Variant'] == Variant.KEEP_INDEX:
            modified_col = df_to_relabel[kwargs['scope_column']].apply(
                get_scope_by_index, indexes=kwargs['sc_indexes'])
        elif kwargs['Variant'] == Variant.KEEP_LEFT:
            modified_col = df_to_relabel[kwargs['scope_column']].apply(
                keep_n_levels, n=kwargs['n'])
        elif kwargs['Variant'] == Variant.KEEP_RIGHT:
            modified_col = df_to_relabel[kwargs['scope_column']].apply(
                keep_n_levels, n=kwargs['n'], left_side=False)
        elif kwargs['Variant'] == Variant.REMOVE_LEFT:
            modified_col = df_to_relabel[kwargs['scope_column']].apply(
                remove_n_levels, n=kwargs['n'])
        elif kwargs['Variant'] == Variant.REMOVE_RIGHT:
            modified_col = df_to_relabel[kwargs['scope_column']].apply(
                remove_n_levels, n=kwargs['n'], left_side=False)
        # TODO remove index does not work yet
        # elif kwargs['Variant'] == Variant.REMOVE_INDEX:
        #     modified_col = df_to_relabel[kwargs['scope_column']].apply(
        #         remove_scope_by_index, indexes=kwargs['sc_indexes'])
        if new_column.any():
            new_column = [str(x) + '/' + str(y)
                          for x, y in zip(new_column, modified_col)]
        else:
            new_column = modified_col
        if column in df.columns:
            new_column =  pd.concat([new_column, df[column][~df.index.isin(new_column.index)]])
    df[column] = new_column
    return df


def parse_command(rel_command: str):
    print(rel_command)
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
    #TODO: not here but relabelling does not need selected scope
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
        df = relabel_function(log.events, **kwargs)
        log.events = df
    elif kwargs['is_object_transformation']:
        print(kwargs)
        df = log.objects.copy() #TODO: probably prone to mistakes with multiple scopes
        df = relabel_function(df, column='new:column', **kwargs)
        log.objects = df
        print(log.objects)
    return log
