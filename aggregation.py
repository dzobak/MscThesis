import pandas as pd
import re
from functions import *


def get_values_mapping(row, old_ids_column, new_id_column) -> dict:
    return {old_id: row[new_id_column] for old_id in row[old_ids_column]}


def map_ids(df, column, values_mapping):
    new_df = pd.DataFrame(columns=df.columns)
    for row in df.itertuples(index=False):
        loc = df.columns.get_loc(column)
        if row[loc] in values_mapping:
            new_row = list(row)
            new_row[loc] = values_mapping[row[loc]]
            new_df.loc[len(new_df.index)] = new_row
    return new_df

# For aggregation, checks if all the values provided in the series are the same


def is_unique(s: pd.Series):
    a = s.to_numpy()
    return (a[0] == a).all()


def truncate_lvl(scope_str, level):
    scope_tuple = get_scope_tuple(scope_str)
    truncated_scope = '/'.join(scope_tuple[:level+1])
    return truncated_scope


def get_scope_equality_level(scope_df):
    # holds the value until which scope level the scope should be truncated
    scope_equality_lvl = -1
    for i in range(len(scope_df.columns)):
        if not is_unique(scope_df[i]):
            scope_equality_lvl = i-1
            break
        elif i == len(scope_df.columns)-1:  # Maybe put for-else here
            scope_equality_lvl = i
    return scope_equality_lvl

# Lowest common Ancestor


def truncate(series):
    # After truncating, all scopes will be the same, so a representative is picked
    first_scope = series.iloc[0]

    tuple_series = series.apply(get_scope_tuple)
    scope_df = pd.DataFrame(tuple_series.to_list())
    scope_equality_lvl = get_scope_equality_level(scope_df)

    truncated_scope = truncate_lvl(first_scope, scope_equality_lvl)

    return truncated_scope

# For Aggregation


def dtype_to_func(col, dtype):
    if re.search(r'scope', col, re.IGNORECASE):
        return truncate
    elif dtype == type(''):
        return lambda x: pd.Series.mode(x)[0]
    elif dtype == type(3) or dtype == type(3.0):
        return 'sum'


def setify(series):
    new_set = set()
    for value in series:
        new_set.add(value)
    return new_set


def aggregate_events(log, **kwargs):
    col_func_map = {}
    special_columns = {
        'id_column': 'ocel:eid',
        'ts_column': 'ocel:timestamp',
        'act_column': 'ocel:activity',
    }

    log.events[log.event_id_column] =\
        log.events[log.event_id_column].astype(float)
    log.relations[log.event_id_column] =\
        log.relations[log.event_id_column].astype(float)
    log.events['Scope1'] = log.events[kwargs['scope_column']]
    print('Scope examples: ')
    for i in range(5):
        print(log.events[kwargs['scope_column']][i*5])

    sc_lvl = int(input('Select the scope level: '))

    for col in log.events.columns:
        if col not in special_columns.values():
            col_func_map[col] = dtype_to_func(col, type(log.events[col][0]))

    col_func_map[log.event_id_column] = ['min', setify]
    col_func_map[log.event_timestamp] = ['min', 'max']

    # TODO: needs to be changed to scope
    col_func_map[log.event_activity] = lambda x: pd.Series.mode(x)[0]

    log.events[kwargs['scope_column']] = log.events[kwargs['scope_column']].apply(
        truncate_lvl, level=sc_lvl)

    agg_events = log.events.groupby([kwargs['scope_column'],
                                    pd.Grouper(key=log.event_timestamp,
                                    freq='20h')], as_index=False).agg(col_func_map)

    new_columns = []
    for x in agg_events.columns:
        if x == (log.event_timestamp, 'min'):
            new_columns.append(log.event_timestamp + ':start')
        elif x == (log.event_id_column, 'setify'):
            new_columns.append('old_ids')
        else:
            new_columns.append(x[0])
    agg_events.columns = new_columns
    agg_events.sort_values(
        log.event_id_column, inplace=True, ignore_index=True)

    # change relations eid column
    value_mapping = agg_events.apply(
        get_values_mapping, axis=1, old_ids_column='old_ids', new_id_column=log.event_id_column)
    value_mapping = value_mapping.aggregate(concat_dicts)
    log.relations = map_ids(
        log.relations, log.event_id_column, value_mapping)

    log.events = agg_events.drop(columns='old_ids')

    # change relation columns besides id
    log.relations[log.event_activity] = log.relations[log.event_id_column].map(
        log.events.set_index(log.event_id_column)[log.event_activity])
    log.relations[log.event_timestamp] = log.relations[log.event_id_column].map(
        log.events.set_index(log.event_id_column)[log.event_timestamp])
    log.relations.drop_duplicates(inplace=True)
    log.relations.reset_index(drop=True, inplace=True)
    print(log.events)
    print(log.relations)
    return log


def aggregate_objects(log, **kwargs):
    col_func_map = {}
    special_columns = {
        'id_column': 'ocel:oid',
    }
    col_func_map[log.object_id_column] = ['min', setify]

    for col in log.objects.columns:
        if col not in special_columns.values():
            col_func_map[col] = dtype_to_func(col, type(log.objects[col][0]))

    print('Scope examples: ')
    for i in range(5):
        print(log.objects[kwargs['scope_column']][i*5 % len(log.objects)])

    sc_lvl = int(input('Select the scope level: '))
    agg_objs = log.objects[log.objects[kwargs['object_column']]
                           == kwargs['object_type']]

    not_agg_objs = log.objects[log.objects[kwargs['object_column']]
                               != kwargs['object_type']]
    agg_objs[kwargs['scope_column']] = agg_objs[kwargs['scope_column']].apply(
        truncate_lvl, level=sc_lvl)
    agg_objs = agg_objs.groupby(
        [kwargs['scope_column']], as_index=False).agg(col_func_map)
    print(agg_objs)

    # change oid in relations table
    value_mapping = agg_objs.apply(get_values_mapping, axis=1, old_ids_column=(
        log.object_id_column, 'setify'), new_id_column=(log.object_id_column, 'min'))
    value_mapping = value_mapping.aggregate(concat_dicts)
    log.relations = map_ids(
        log.relations, log.object_id_column, value_mapping)

    agg_objs = agg_objs.drop(columns=(log.object_id_column, 'setify'))
    agg_objs = agg_objs.droplevel(1, axis=1)
    agg_objs.sort_values(
        log.object_id_column, inplace=True, ignore_index=True)

    log.objects = pd.concat([agg_objs, not_agg_objs])

    log.relations.drop_duplicates(inplace=True)
    log.relations.reset_index(drop=True, inplace=True)

    print(log.objects)
    print(log.relations.head(30))

    return log


def execute_aggregation(log, **kwargs):

    if kwargs['evt_or_obj'] == 'e':
        agg_log = aggregate_events(log, **kwargs)
    elif kwargs['evt_or_obj'] == 'o':
        agg_log = aggregate_objects(log, **kwargs)

    return agg_log
