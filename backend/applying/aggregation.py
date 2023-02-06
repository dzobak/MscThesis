import pandas as pd
from applying.aggregation_keys import get_aggregation_key_by_rules
from utils import *
from enum import Enum
from pandas.core.series import Series


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


def truncate(series):
    """Input: Series with scopes as values
    Output: Series with scopes as values. All scopes are shortened until they match or are empty. That means all scopes have the same value.

    Truncating follows the idea of finding the common lowest ancestor.
    """
    # After truncating, all scopes will be the same, so a representative is picked
    print(series)
    first_scope = series.iloc[0]
    tuple_series = series.apply(get_scope_tuple)
    scope_df = pd.DataFrame(tuple_series.to_list())
    scope_equality_lvl = get_scope_equality_level(scope_df)

    truncated_scope = keep_n_levels(first_scope, n=scope_equality_lvl+1)

    return truncated_scope

# For Aggregation


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


def aggregate_events(log, **kwargs):
    col_func_map = kwargs['col_func_map']
    # TODO where col func is groupby need to add as key, where col func is discard need to remove from col_func

    col_func_map_mod = {k: get_aggregation_functions(
        v) for k, v in col_func_map.items() if get_aggregation_functions(v) is not None}
    col_func_map_mod[log.event_id_column] = [
        col_func_map_mod[log.event_id_column], setify]

    log.events[kwargs['scope_column']] = log.events[kwargs['scope_column']].apply(
        keep_n_levels, n=kwargs['scope_level']+1)

    # need to redo the group by keys to allow more options
    group_by_keys = [kwargs['scope_column']]

    if len(kwargs['rules']):
        kwargs['id_column'] = log.event_id_column
        group_by_keys = []
        for name, group in log.events.groupby(kwargs['scope_column'], as_index=False):
            group_by_keys.append(get_aggregation_key_by_rules(group, **kwargs))

        group_by_keys = concat_dicts(pd.Series(group_by_keys))
    print(group_by_keys)

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
    """Enum containing aggregation methods that are available for different data types"""
    SUM = Series.sum
    MIN = Series.min
    MAX = Series.max
    AVG = Series.mean
    MEDIAN = Series.median
    def MODE(x): return pd.Series.mode(x)
    TRUNCATE = truncate
    COUNT = Series.count
    def CONCAT(x): return pd.Series.str.cat(x)
