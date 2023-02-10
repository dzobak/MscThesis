import operator
from typing import List
import pandas as pd
from pandas.api.indexers import BaseIndexer
import numpy as np
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
    if current_value != current_value:  # check if nan
        current_value = ''
    # TODO make work with scopes
    if rule['unified'] == 'unified':
        if type(cluster.iloc[0]) == str:
            return negation(op(set([current_value]), set(cluster)))
        else:
            return negation(op(set(current_value), setify_values(cluster)))
    else:
        result = True
        for value in cluster:
            if result:
                result = negation(op(set(current_value), set(value)))
            else:
                break
        print(result)
        return result


def evaluate_rules(rules: List[dict], df: pd.DataFrame, current_idx: int, first_idx: int) -> bool:
    results = []
    for rule in rules.values():
        op = get_operator_fnc(rule['operator'])
        negation = operator.not_ if rule['bool'] == 'not' else same
        if rule['type'] == 'timestamp' or rule['type'] == 'numerical':
            if rule['compared'] == 'first':
                compared = first_idx
            elif rule['compared'] == 'last':
                compared = current_idx-1
            if rule['type'] == 'timestamp':
                results.append(negation(op(pd.to_timedelta(
                    df[rule['attribute']].iloc[current_idx] - df[rule['attribute']].iloc[compared]), pd.to_timedelta(rule['value']))))
            elif rule['type'] == 'numerical':
                results.append(negation(
                    op(df[rule['attribute']].iloc[current_idx]-df[rule['attribute']].iloc[compared], rule['value'])))
        elif rule['type'] == 'categorical' or rule['type'] == 'object':
            results.append(check_categorical_rule(df[rule['attribute']].iloc[first_idx:current_idx],
                                                  df[rule['attribute']].iloc[current_idx], **rule))
        elif rule['type'] == 'scope':
            results.append(check_categorical_rule(df[rule['attribute']].apply(get_scope_by_index, indexes=[int(rule['level'])]).iloc[first_idx:current_idx],
                                                  df[rule['attribute']].apply(get_scope_by_index, indexes=[int(rule['level'])]).iloc[current_idx], **rule))

    return any(results)


def get_aggregation_key_by_rules(df, **kwargs):
    # partition by other attributes
    # I can do whatever here, don't think of window functions as a simple iterator
    # statement = evaluate_rules(kwargs['rules'])
    num_values = len(df.index)
    keys = {}
    j = 0  # position of first element of cluster
    for i in range(0, num_values):
        if i > 0:
            # if any rule is true create new cluster
            if evaluate_rules(kwargs['rules'], df, i, j):
                j = i
        keys[df.index[i]] = df[kwargs['id_column']].iloc[j]
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
