import pandas as pd
import re
from utils import *
from enum import Enum
from pandas.core.series import Series
import json


def get_old_to_new_id_mapping(row: pd.Series, old_ids_column: str, new_id_column: str) -> dict:
    return {old_id: row[new_id_column] for old_id in row[old_ids_column]}


def get_new_to_old_id_mapping(row: pd.Series, old_ids_column: str, new_id_column: str) -> dict:
    return {row[new_id_column]: list(row[old_ids_column])}


def map_ids(df: pd.DataFrame, column: str, values_mapping: dict) -> pd.DataFrame:
    new_df = pd.DataFrame(columns=df.columns)
    for row in df.itertuples(index=False):
        loc = df.columns.get_loc(column)
        if row[loc] in values_mapping:
            new_row = list(row)
            new_row[loc] = values_mapping[row[loc]]
            new_df.loc[len(new_df.index)] = new_row
    return new_df

# For aggregation, checks if all the values provided in the series are the same


def is_unique(s: pd.Series) -> bool:
    """
    Input: pandas Series

    Output: True if all values of the Series are the same, False otherwise
    """
    a = s.to_numpy()
    return (a[0] == a).all()


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

    truncated_scope = keep_n_levels(first_scope, n=scope_equality_lvl+1)

    return truncated_scope

# For Aggregation


# def dtype_to_func_defaults(col, dtype):
#     if re.search(r'scope', col, re.IGNORECASE):
#         return truncate
#     elif dtype == type(''):
#         return lambda x: pd.Series.mode(x)[0]
#     elif dtype == type(3) or dtype == type(3.0):
#         return 'sum'


def get_aggregation_functions(keyword: str):
    """
    Input: Keyword referring to a function

    Output: Function that was specified by keyword
    """
    # TODO group by and discard need to be dealt with differently (I think discard is handled)
    if keyword == 'SUM':
        return Method.SUM
    elif keyword == 'MIN':
        return Method.MIN
    elif keyword == 'MAX':
        return Method.MAX
    elif keyword == 'MIN and MAX':
        return [Method.MIN, Method.MAX]
    elif keyword == 'AVG':
        return Method.AVG
    elif keyword == 'MEDIAN':
        return Method.MEDIAN
    elif keyword == 'MODE':
        return Method.MODE
    elif keyword == 'TRUNCATE':
        return Method.TRUNCATE
    elif keyword == 'CONCAT':
        return Method.CONCAT
    elif keyword == 'COUNT':
        return Method.COUNT


def setify(series):
    new_set = set()
    for value in series:
        new_set.add(value)
    return new_set


def aggregate_events(log, **kwargs):
    col_func_map = kwargs['col_func_map']
    # TODO where col func is groupby need to add as key, where col func is discard need to remove from col_func

    col_func_map_mod = {k: get_aggregation_functions(
        v) for k, v in col_func_map.items() if get_aggregation_functions(v) is not None}
    col_func_map_mod[log.event_id_column] = [
        col_func_map_mod[log.event_id_column], setify]

    log.events[kwargs['scope_column']] = log.events[kwargs['scope_column']].apply(
        keep_n_levels, n=kwargs['scope_level']+1)

    #need to redo the group by keys to allow more options
    group_by_keys = [kwargs['scope_column']]
    if len(kwargs['grouping_key']):
        group_by_keys.append(pd.Grouper(
            key=log.event_timestamp, freq=kwargs['grouping_key']))

    # TODO when values of col_func_map group by then add to
    agg_events = log.events.groupby(
        group_by_keys, as_index=False).agg(col_func_map_mod)

    new_columns = []
    for x in agg_events.columns:
        if x == (log.event_timestamp, 'min') and (log.event_timestamp, 'max') in agg_events.columns:
            # TODO update OCEL extension to allow for multiple timestamps
            new_columns.append('start:' + log.event_timestamp)
        elif x == (log.event_id_column, 'setify'):
            new_columns.append('old_ids')
        else:
            new_columns.append(x[0])
    agg_events.columns = new_columns
    agg_events.sort_values(
        log.event_id_column, inplace=True, ignore_index=True)

    # change relations eid column
    old_to_new_id_mapping = agg_events.apply(
        get_old_to_new_id_mapping, axis=1, old_ids_column='old_ids', new_id_column=log.event_id_column)
    old_to_new_id_mapping = old_to_new_id_mapping.aggregate(concat_dicts)

    new_to_old_id_mapping = agg_events.apply(
        get_new_to_old_id_mapping, axis=1, old_ids_column='old_ids', new_id_column=log.event_id_column)
    new_to_old_id_mapping = new_to_old_id_mapping.aggregate(concat_dicts)

    log.relations = map_ids(
        log.relations, log.event_id_column, old_to_new_id_mapping)

    log.events = agg_events.drop(columns='old_ids')

    # change relation columns besides id
    log.relations[log.event_activity] = log.relations[log.event_id_column].map(
        log.events.set_index(log.event_id_column)[log.event_activity])
    log.relations[log.event_timestamp] = log.relations[log.event_id_column].map(
        log.events.set_index(log.event_id_column)[log.event_timestamp])
    log.relations.drop_duplicates(inplace=True)
    log.relations.reset_index(drop=True, inplace=True)

    return log, new_to_old_id_mapping


def aggregate_objects(log, **kwargs):
    col_func_map = kwargs['col_func_map']

    col_func_map_mod = {k: get_aggregation_functions(
        v) for k, v in col_func_map.items() if get_aggregation_functions(v) is not None}
    col_func_map_mod[log.object_id_column] = [
        col_func_map_mod[log.object_id_column], setify]

    agg_objs = log.objects[log.objects[log.object_type_column]
                           == kwargs['object_type']]

    not_agg_objs = log.objects[log.objects[log.object_type_column]
                               != kwargs['object_type']]
    agg_objs[kwargs['scope_column']] = agg_objs[kwargs['scope_column']].apply(
        keep_n_levels, n=kwargs['scope_level']+1)

    agg_objs = agg_objs.groupby(
        [kwargs['scope_column'], log.object_type_column, ], as_index=False).agg(col_func_map_mod)

    # change oid in relations table
    old_to_new_id_mapping = agg_objs.apply(get_old_to_new_id_mapping, axis=1, old_ids_column=(
        log.object_id_column, 'setify'), new_id_column=(log.object_id_column, 'min'))
    old_to_new_id_mapping = old_to_new_id_mapping.aggregate(concat_dicts)
    log.relations = map_ids(
        log.relations, log.object_id_column, old_to_new_id_mapping)

    agg_objs = agg_objs.drop(columns=(log.object_id_column, 'setify'))
    agg_objs = agg_objs.droplevel(1, axis=1)

    agg_objs.sort_values(
        log.object_id_column, inplace=True, ignore_index=True)

    log.objects = pd.concat([agg_objs, not_agg_objs])
    # log.objects = agg_objs
    # TODO need to further look into nan values
    log.objects.replace({np.nan: None}, inplace=True)

    log.relations.drop_duplicates(inplace=True)
    log.relations.reset_index(drop=True, inplace=True)

    return log


def execute_aggregation(log, **kwargs):
    if kwargs['is_event_transformation']:
        agg_log, new_to_old_id_mapping = aggregate_events(log, **kwargs)
    elif kwargs['is_object_transformation']:
        agg_log = aggregate_objects(log, **kwargs)
    else:
        raise Exception("Objects or Events need to be selected")

    return agg_log, new_to_old_id_mapping

class Method(Enum):
    """Aggregation methods that are available for different data types"""
    SUM = Series.sum
    MIN = Series.min
    MAX = Series.max
    AVG = Series.mean
    MEDIAN = Series.median
    def MODE(x): return pd.Series.mode(x)
    TRUNCATE = truncate
    COUNT = Series.count
    def CONCAT(x): return pd.Series.str.cat(x)
