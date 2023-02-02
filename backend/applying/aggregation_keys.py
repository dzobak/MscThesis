import pandas as pd
from pandas.api.indexers import BaseIndexer
import numpy as np


def translate_kwd(kwd: str) -> str:
    if kwd == 'last':
        return "i-1"
    elif kwd == 'first':
        return "j"
    elif kwd == '\u2264':
        return "<="
    elif kwd == '\u2265':
        return ">="


def parse_rules(rules):
    command = ""
    for rule in rules.values():
        # only supports timestamps for now
        # time = pd.to_timedelta(rule['value'])
        command += "pd.to_timedelta(df['" + rule['attribute'] + "'].iloc[i]-df['" + rule['attribute'] + \
            "'].iloc[" + translate_kwd(rule['compared'])+"]) " + rule['bool'] + " " + \
            translate_kwd(rule['operator']) + \
            " pd.to_timedelta('" + rule['value'] + "') and "
    command = command[:-4]
    return command


def get_aggregation_key_by_rules(df, **kwargs):
    # partition by other attributes
    # I can do whatever here, don't think of window functions as a simple iterator
    statement = parse_rules(kwargs['rules'])
    num_values = len(df.index)
    keys = {}
    j = 0
    for i in range(0, num_values):
        if i > 0:
            if eval(statement):
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
