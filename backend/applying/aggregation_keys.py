from typing import List
import pandas as pd
from pandas.api.indexers import BaseIndexer
import numpy as np


def translate_kwd(kwd: str) -> str:
    if kwd == 'last':
        return "i-1"
    elif kwd == 'first':
        return "j"
    #the lists or items need to be converted to sets, for subset operators    
    elif kwd in ['\u2264','\u2286']:
        return "<="
    elif kwd in ['\u2265','\u2287']:
        return ">="
    else: return kwd


def check_categorical_rule(cluster:pd.Series,current_value:str, **kwargs)->bool:
    """
    Input: cluster, current value, and kwargs including keys: bool, operator, compared, unified and optionaly: level and n
    Output: True, if rule is fullfilled, False if not
    """   
    pass

def parse_rules(rules)->str:
    command = ""
    for rule in rules.values():
        # only supports timestamps for now
        # time = pd.to_timedelta(rule['value'])
        if rule['type'] == 'timestamp':
            command += "pd.to_timedelta(df['" + rule['attribute'] + "'].iloc[i]-df['" + rule['attribute'] + \
                "'].iloc[" + translate_kwd(rule['compared'])+"]) " + rule['bool'] + " " + \
                translate_kwd(rule['operator']) + \
                " pd.to_timedelta('" + rule['value'] + "') or "
        elif rule['type'] == 'numerical':
            command += "df['" + rule['attribute'] + "'].iloc[i]-df['" + rule['attribute'] + \
                "'].iloc[" + translate_kwd(rule['compared'])+"] " + rule['bool'] + " " + \
                translate_kwd(rule['operator']) + " " + rule['value'] + " or "
        elif rule['type'] == 'categorical':
            command += "check_categorical_rule(df[rule['attribute'].iloc[j:i],df[rule['attribute'].iloc[i], **rule]) or "
            pass
    if len(command) > 3:
        command = command[:-3]
    else: command = "False"
    return command


def get_aggregation_key_by_rules(df, **kwargs):
    # partition by other attributes
    # I can do whatever here, don't think of window functions as a simple iterator
    statement = parse_rules(kwargs['rules'])
    num_values = len(df.index)
    keys = {}
    j = 0 #position of first element of cluster
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
