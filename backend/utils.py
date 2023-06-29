from typing import List
import pandas as pd
import os
from OCEL_extended import OCEL_ext
import numpy as np
import networkx as nx


def get_scope_tuple(scope: str, sep='/') -> tuple:
    scope_tup = tuple(scope.rsplit(sep)) if type(scope) == str else tuple()
    return scope_tup


def get_max_scope_depth(series: pd.Series):
    tuple_series = series.apply(get_scope_tuple)
    return max([len(x) for x in tuple_series])


def concat_dicts(iterable) -> dict:
    new_dict = {}
    for dict in iterable:
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
        truncated_scope = '/'.join(scope_tuple[:n])
    else:
        truncated_scope = '/'.join(scope_tuple[-n:])
    return truncated_scope


def remove_n_levels(scope_str: str, n: int, left_side=True) -> str:
    scope_tuple = get_scope_tuple(scope_str)
    n = min(len(scope_tuple), n)
    if left_side:
        truncated_scope = '/'.join(scope_tuple[n:])
    else:
        truncated_scope = '/'.join(scope_tuple[:-n])
    return truncated_scope


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


def setify(series: pd.Series) -> set:
    new_set = set()
    for value in series:
        new_set.add(value)
    return new_set


def setify_values(series: pd.Series) -> set:
    new_set = set()
    for value in series:
        if value == value:
            for subvalue in set(value):
                if subvalue == subvalue:  # no nan values
                    new_set.add(subvalue)
    return new_set


def get_file_folder() -> str:
    return os.path.join('backend','event_log_files', '')


def get_log_filepath_from_name(name: str) -> str:
    return os.path.join('.', 'backend' , 'event_log_files', name+'.jsonocel')


def get_image_filepath_from_name(name: str) -> str:
    return os.path.join('.','backend', 'images', name+'.png')


def get_image_link_from_name(name: str) -> str:
    return 'http://127.0.0.1:5002/images/' + name


def get_name_from_filepath(path: str, filetype='jsonocel') -> str:
    folder = get_file_folder()
    name = path.split(folder)[1]
    name = name.split('.'+filetype)[0]
    return name


def get_column_functions_by_dtype(dtype: type) -> List[str]:
    if dtype == type(''):
        return ['MODE', 'CONCAT', 'MAX', 'MIN', 'DISCARD']
    # TODO: Nan values can by identified as number even if the rest of the column is string
    elif dtype == type(0) or dtype == type(1.0) or np.issubdtype(dtype, np.number):
        return ['SUM', 'MAX', 'MIN', 'COUNT', 'AVG', 'MEDIAN', 'MODE', 'DISCARD']
    print(dtype)
    return ["good job"]


def get_column_function_options(log: OCEL_ext, **kwargs) -> dict:
    col_functions = {}
    if kwargs['is_event_transformation']:
        df = log.events
        col_functions[log.event_id_column] = ['MIN', 'MAX', 'MODE']
        col_functions[log.event_timestamp] = ['MIN and MAX', 'MIN', 'MAX']
        col_functions[log.event_activity] = ['TRUNCATE'] if log.event_activity in log.event_scope_columns\
            else ['GROUP BY']

        for scope in log.event_scope_columns:
            if scope not in col_functions:
                col_functions[scope] = ['TRUNCATE', 'MODE', 'COUNT', 'DISCARD']

        object_type_columns = log.get_object_type_column_names()
        for col in object_type_columns:
            col_functions[col] = ['UNION']

    elif kwargs['is_object_transformation']:
        df = log.objects
        col_functions[log.object_id_column] = ['MIN', 'MAX', 'MODE']
        col_functions[log.object_type_column] = ['GROUP BY']

        for scope in log.object_scope_columns:
            if scope not in col_functions:
                col_functions[scope] = ['TRUNCATE', 'GROUP BY', 'DISCARD']

    for column in df.columns:
        if column not in col_functions:
            print(df[column].dtypes)
            col_functions[column] = get_column_functions_by_dtype(
                type(df.iloc[df[column].first_valid_index()][column]))
    return col_functions


def get_column_dtypes(log: OCEL_ext) -> dict:
    column_dtypes = {}
    object_type_columns = log.get_object_type_column_names()
    events = log.get_extended_table()
    for df in [events, log.objects]:
        for column in df.columns:
            dtype = type(df.iloc[df[column].first_valid_index()][column])
            if column in log.event_scope_columns or column in log.object_scope_columns:
                column_dtypes[column] = 'scope'
            elif dtype == type(''):
                column_dtypes[column] = 'categorical'
            elif dtype == type(0) or dtype == type(1.0) or np.issubdtype(dtype, np.number):
                column_dtypes[column] = 'numeric'
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                column_dtypes[column] = 'timestamp'
            elif column in object_type_columns:
                column_dtypes[column] = 'object'
    return column_dtypes


def same(x):
    """returns the input back"""
    return x


def rename_file(old_name: str, new_name: str) -> None:
    os.rename(get_log_filepath_from_name(old_name),
              get_log_filepath_from_name(new_name))


def delete_file(name: str) -> None:
    os.remove(get_log_filepath_from_name(name))

def get_scope_list(scope: str, sep='/') -> list:
    scope_list = list(scope.rsplit(sep)) if type(scope) == str else []
    return scope_list

def get_nodes_and_edges(scopes: pd.Series):
    print(scopes)
    scope_groups = scopes.groupby(scopes).count()
    scope_pairs = []
    weight = []
    tmp_nodes = set()
    for scope in scope_groups.index:
        if scope:
            scope_list = get_scope_list(scope)
            for i in range(len(scope_list)):
                # nodes[scope_list[i]]= i
                if i == 0:
                    scope_pairs.append(('n0', scope_list[i]))
                    weight.append(scope_groups[scope])
                elif i < len(scope_list):
                    scope_pairs.append(('/'.join(scope_list[:i]), '/'.join(scope_list[:i+1])))
                    weight.append(scope_groups[scope])
                tmp_nodes.add(tuple(scope_list[:i+1]))
    
    nodes = []
    for tup in tmp_nodes:
        nodes.append(('/'.join(tup), {'label': tup[-1]}))
    
    edges = pd.DataFrame({'scope_pairs': scope_pairs, 'weight': weight})
    edges = edges.groupby('scope_pairs', as_index=False).sum('weight')
    return nodes,edges


def get_scope_graph(scopes: pd.Series, eventlogname: str):
    nodes,edges = get_nodes_and_edges(scopes)
    G = nx.DiGraph()

    G.add_nodes_from(nodes)

    for idx, edge in edges.iterrows():
        G.add_edge(*edge['scope_pairs'], label=edge['weight'])

    A = nx.nx_agraph.to_agraph(G)
    A.node_attr["shape"] = "box"
    print(A.string())
    n = A.get_node('n0')
    n.attr['style'] = 'invis'
    A.layout("dot")  # layout with dot
    name = eventlogname + '-' + scopes.name
    path = get_image_filepath_from_name(name)
    A.draw(path)
    return get_image_link_from_name(name)
