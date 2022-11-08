import pm4py 
from pm4py.objects.ocel.importer import jsonocel
import re
import pandas as pd

def get_scope_tuple(scope):
    return tuple(scope.rsplit('/'))

def is_unique(s):
    a = s.to_numpy()
    return (a[0] == a).all()

def truncate_lvl(scope_value,level):
    scope_tuple = get_scope_tuple(scope_value)
    truncated_scope = '/'.join(scope_tuple[:level+1])
    return truncated_scope

def truncate(series):
    first_scope = series.iloc[0] #After truncating, all scopes will be the same, so a representative is picked
    tuple_series = series.apply(get_scope_tuple)
    # first_tuple = tuple_series.iloc[0]
    scope_df = pd.DataFrame(tuple_series.to_list())
    scope_equality_lvl =  -1 #holds the value until which scope level the
    for i in range(len(scope_df.columns)):
        if not is_unique(scope_df[i]):
            scope_equality_lvl = i-1
            break
        elif i == len(scope_df.columns)-1:
            scope_equality_lvl = i
    
    # truncated_scope = ""
    # for i in range(scope_equality_lvl+1):
    #     truncated_scope += first_tuple[i] + "/"
    truncated_scope = truncate_lvl(first_scope, scope_equality_lvl)
            
    return truncated_scope

def dtype_to_func(col,dtype):
    if re.search(r"scope", col):
        return truncate
    elif dtype == type(""):
        return 'mode'
    elif dtype == type(3) or dtype == type(3.0):
        return 'sum'
    

def aggregation(log):
    agg = "events"
    
    col_func_map = {}
    if agg == "events":
        special_columns = {
            "id_column": "ocel:eid",
            "ts_column": "ocel:timestamp",
            "act_column": "ocel:activity",
            "sc_column": str(input("Select scope column: "))
            }
        print("Scope examples: ")

        log.events["scope1"] = log.events[special_columns["sc_column"]]
        for i in range(5):
            print(log.events[special_columns["sc_column"]][i*5])
        
        sc_lvl = int(input("Select the scope level: ")) 

        for col in log.events.columns:
            if col not in special_columns.values():
                col_func_map[col] = dtype_to_func(col,type(log.events[col][0]))
            
            
        col_func_map[special_columns["id_column"]] = "min"
        col_func_map[special_columns["ts_column"]] = ['min','max']
        
        log.events[special_columns["sc_column"]] = log.events[special_columns["sc_column"]].apply(truncate_lvl, level=sc_lvl)
        
        agg_log = log.events.groupby(special_columns["sc_column"]).agg(col_func_map)

        
    print(col_func_map)
    print(agg_log)
    



# filepath = str(input("Filepath: "))
filepath = "/Users/dzoba/Studies/MasterThesis/Preparation/toy_log2.jsonocel"
method =  str(input("Selection function(s) or aggregation(a): "))

log = jsonocel.importer.apply(filepath)
log_df = log.get_extended_table()

print(log_df.columns)

if method == "s":
    print("s")
elif method == "a":
    aggregation(log)
elif method =="t":
    print(type(log.events["scope"]))
    print(truncate(log.events["scope"]))
else:
    print("wrong method")



