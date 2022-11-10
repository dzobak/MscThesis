import pm4py 
from pm4py.objects.ocel.importer import jsonocel
import re
import pandas as pd
import scipy

#For aggregation and relabelling
def get_scope_tuple(scope):
    return tuple(scope.rsplit('/'))

#For aggregation, checks if all the values provided in the series are the same
def is_unique(s:pd.Series):
    a = s.to_numpy()
    return (a[0] == a).all()

def truncate_lvl(scope_value,level):
    scope_tuple = get_scope_tuple(scope_value)
    truncated_scope = '/'.join(scope_tuple[:level+1])
    return truncated_scope

def truncate(series):
    first_scope = series.iloc[0] #After truncating, all scopes will be the same, so a representative is picked
    
    tuple_series = series.apply(get_scope_tuple)
    scope_df = pd.DataFrame(tuple_series.to_list())
    
    scope_equality_lvl =  -1 #holds the value until which scope level the scope should be truncated
    for i in range(len(scope_df.columns)):
        if not is_unique(scope_df[i]):
            scope_equality_lvl = i-1
            break
        elif i == len(scope_df.columns)-1:
            scope_equality_lvl = i
    
    truncated_scope = truncate_lvl(first_scope, scope_equality_lvl)
            
    return truncated_scope

#For Aggregation
def dtype_to_func(col,dtype):
    if re.search(r"scope", col, re.IGNORECASE):
        return truncate
    elif dtype == type(""):
        return 'mode'
    elif dtype == type(3) or dtype == type(3.0):
        return 'sum'
    

def aggregation(log, scope_column):
    agg = "events"
    
    col_func_map = {}
    if agg == "events":
        special_columns = {
            "id_column": "ocel:eid",
            "ts_column": "ocel:timestamp",
            "act_column": "ocel:activity",
            "sc_column": scope_column
            }
        print("Scope examples: ")

        log.events[special_columns["id_column"]] = log.events[special_columns["id_column"]].astype(float) 
        log.events["Scope1"] = log.events[special_columns["sc_column"]]
        for i in range(5):
            print(log.events[special_columns["sc_column"]][i*5])
        
        sc_lvl = int(input("Select the scope level: ")) 

        for col in log.events.columns:
            if col not in special_columns.values():
                col_func_map[col] = dtype_to_func(col,type(log.events[col][0]))
            
            
        col_func_map[special_columns["id_column"]] = "min"
        col_func_map[special_columns["ts_column"]] = ['min','max']
        col_func_map[special_columns["act_column"]] = lambda x: pd.Series.mode(x)[0]

        log.events[special_columns["sc_column"]] = log.events[special_columns["sc_column"]].apply(truncate_lvl, level=sc_lvl)
        
        agg_log = log.events.groupby([special_columns["sc_column"],
            pd.Grouper(key=special_columns["ts_column"], freq='20h')],
            as_index=False).agg(col_func_map)

        # agg_log.columns[3] = ('ocel:timestamp:start', 'min')
        # agg_log.columns.set_levels()
        # agg_log.index = agg_log.index.to_frame()
        new_columns = []
        for x in agg_log.columns:
            if x == (special_columns["ts_column"],'min'):
                new_columns.append(special_columns["ts_column"] + ':start')
            else:
                new_columns.append(x[0])
        agg_log.columns = new_columns   
        agg_log.sort_values(special_columns["id_column"], inplace=True, ignore_index=True)
        # agg_log.reindex()
        
    # print(col_func_map)
    print(agg_log)
    print(agg_log.columns)
    
def compare_paths(path1, path2):
        if re.search(path2,path1):
            return True
        else:
            return False

# "*" means any deepness of scope is allowed 
def selection_function(regex :str, df: pd.DataFrame ,scope_column: str, scope_sep = "/"):
    scope = df[scope_column]
    regex = re.sub("\?"+ scope_sep,'((\\\w+|\\\s)+'+scope_sep+')?',regex)
    regex = re.sub("\*" + scope_sep,'(.*'+scope_sep+')*',regex)
    print(regex)
    paths = scope.apply(compare_paths, path2=(regex))
    paths = paths[paths] #Only where values True i.e. paths match
    return df.loc[paths.index]


# filepath = str(input("Filepath: "))
filepath = "/Users/dzoba/Studies/MasterThesis/Preparation/toy_log2.jsonocel"
method =  str(input("Selection function (s), aggregation (a) or relabelling (r): "))
if method not in ["s","a","r","test"]:
    print("wrong method")
else:
    log = jsonocel.importer.apply(filepath)
    log_df = log.get_extended_table()

    print(log_df.columns)

    scope_column = str(input("Select scope column: ")) 

if method == "s":
    regex = str(input("Specify regex: ")) 
    print(selection_function(regex, log.get_extended_table(),scope_column))
elif method == "a":
    aggregation(log, scope_column)
elif method == 'r':
    print('r')
elif method =="test": 
    print(type(log.events["scope"]))
    print(truncate(log.events["scope"]))
