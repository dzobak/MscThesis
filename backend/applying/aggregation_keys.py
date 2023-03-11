import operator
from typing import List
import pandas as pd
# from pandas.api.indexers import BaseIndexer
# import numpy as np
from utils import setify_values, same, get_scope_by_index


def get_operator_fnc(kwd: str):

    # the lists or items need to be converted to sets, for subset operators
    if kwd in ['\u2264', '\u2286']:
        return operator.le
    elif kwd in ['\u2265', '\u2287']:
        return operator.ge
    elif kwd == '=':
        return operator.eq
    elif kwd == '<':
        return operator.lt
    elif kwd == '>':
        return operator.gt
    else:
        return kwd


def check_categorical_rule(cluster: pd.Series, current_value: str | List[str], **rule) -> bool:
    """
    Output: True, if rule is fullfilled, False if not
    """
    if rule['compared'] == 'first':
        cluster = cluster.iloc[:min(int(rule['value']), len(cluster.index))]
    elif rule['compared'] == 'last':
        cluster = cluster.iloc[-min(int(rule['value']), len(cluster.index)):]

    op = get_operator_fnc(rule['operator'])
    negation = operator.not_ if rule['bool'] == 'not' else same
    if current_value != current_value:
        current_value = ''  # check if nan
    # TODO make work with scopes
    if rule['unified'] == 'unified':
        if type(cluster.iloc[0]) == str:
            return negation(op(set([current_value]), set(cluster)))
        else:
            return negation(op(set(current_value), setify_values(cluster)))
    else:
        result = True
        for value in cluster:
            value = set(value) if value == value else set()
            if result:
                result = negation(op(set(current_value), value))
            else:
                break
        return result


def evaluate_rules(rules: List[dict], df: pd.DataFrame, current_idx: int, indexes: List[int]) -> bool:
    results = []
    first_idx = indexes[0]
    for rule in rules.values():
        op = get_operator_fnc(rule['operator'])
        negation = operator.not_ if rule['bool'] == 'not' else same
        if rule['type'] == 'timestamp' or rule['type'] == 'numerical':
            if rule['compared'] == 'first':
                compared = indexes[0]
            elif rule['compared'] == 'last':
                compared = indexes[-1]

            if rule['type'] == 'timestamp':
                results.append(negation(op(pd.to_timedelta(
                    df[rule['attribute']].iloc[current_idx] - df[rule['attribute']].loc[compared]), pd.to_timedelta(rule['value']))))
            elif rule['type'] == 'numerical':
                results.append(negation(
                    op(df[rule['attribute']].iloc[current_idx]-df[rule['attribute']].loc[compared], rule['value'])))
        elif rule['type'] == 'categorical' or rule['type'] == 'object':
            results.append(check_categorical_rule(df[rule['attribute']].loc[indexes],
                                                  df[rule['attribute']].iloc[current_idx], **rule))
        elif rule['type'] == 'scope':
            results.append(check_categorical_rule(df[rule['attribute']].apply(get_scope_by_index, indexes=[int(rule['level'])]).loc[indexes],
                                                  df[rule['attribute']].apply(get_scope_by_index, indexes=[int(rule['level'])]).iloc[current_idx], **rule))

    return all(results)

def get_last_N_clusters(N:int, keys:dict):
        last_clusters = []  # clusters where the last N elements were added to
        
        #get clusters where the last N events were assigned
        # for j in range(1, min(len(keys), N)+1):
        #     last_clusters.append(list(keys.values())[len(keys)-j])
        
        #get last N clusters
        for j in range(1, len(keys)+1):
            last_clusters.append(list(keys.values())[len(keys)-j])
            last_clusters = list(dict.fromkeys(last_clusters))
            if len(last_clusters) == N:
                break

        last_clusters = list(dict.fromkeys(last_clusters))
        return last_clusters


def get_aggregation_key_by_rules(df, **kwargs):
    num_values = len(df.index)
    keys = {}
    kwargs.setdefault('lastN', 10)

    for i in range(0, num_values):
        last_clusters = get_last_N_clusters(kwargs['lastN'], keys)
        last_cluster_id = df[kwargs['id_column']].iloc[i]
  
        if i > 0:

            for cluster_id in last_clusters:
                indexes = [k for k, v in keys.items() if v == cluster_id]
                # if all rules are true create new cluster
                if evaluate_rules(kwargs['rules'], df, i, indexes):
                    last_cluster_id = cluster_id
                    break

        keys[df.index[i]] = last_cluster_id
        print()

    return keys


# def distance_func(self, val1, val2):
#     return val2-val1


# class distanceToLastIndexer(BaseIndexer):
#     """input: distance func, distance value,df"""

#     def __init__(self, distance_val, distance_func, df: pd.DataFrame):
#         self.distance = distance_val
#         self.distance_func = distance_func
#         self.df = df
#         super.__init__()

#     def get_window_bounds(self, num_values, min_periods, center, closed):
#         start = np.empty(num_values, dtype=np.int64)
#         end = np.empty(num_values, dtype=np.int64)
#         start[0] = 0
#         for i in range(num_values):
#             # will make this condition more flexible in the future
#             if self.distance_func(self.df[self.column][i], self.df[self.column][i+1]) <= self.distance:
#                 start[i+1] = start[i]
#             else:
#                 start[i+1] = i+1
#                 for j in range(start[i], i+1):
#                     end[j] = i+1

#         return start, end
