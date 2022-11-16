import pm4py 
from pm4py.objects.ocel.importer import jsonocel
import re
import pandas as pd

#For aggregation and relabelling
def get_scope_tuple(scope):
    return tuple(scope.rsplit('/'))

def concat_dicts(series):
    new_dict = {}
    for dict in series:
        new_dict = {**new_dict , **dict}
    return new_dict

def get_values_mapping(df,old_ids_column, new_id_column):
    mapping = dict()
    for old_id in df[old_ids_column]:
        mapping[old_id] = df[new_id_column]
    return mapping

def map_ids(df, column, values_mapping):
    new_df = pd.DataFrame(columns=df.columns)
    for i in range(len(df)):
        if (df[column].iloc[i]) in values_mapping:
            df[column].iloc[i] = values_mapping[(df[column].iloc[i])]
            new_df = pd.concat([new_df, df.iloc[i].to_frame().transpose()])
    return new_df

#For aggregation, checks if all the values provided in the series are the same
def is_unique(s:pd.Series):
    a = s.to_numpy()
    return (a[0] == a).all()

def truncate_lvl(scope_value,level):
    scope_tuple = get_scope_tuple(scope_value)
    truncated_scope = '/'.join(scope_tuple[:level+1])
    return truncated_scope

#Lowest common Ancestor
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
        return lambda x: pd.Series.mode(x)[0]
    elif dtype == type(3) or dtype == type(3.0):
        return 'sum'


def setify(series):
    new_set = set()
    for i in range(len(series)):
        new_set.add(series.iloc[i])
    return new_set
    
def aggregate_events(log, **kwargs):
        col_func_map = {}
        special_columns = {
            "id_column": "ocel:eid",
            "ts_column": "ocel:timestamp",
            "act_column": "ocel:activity",
            }

        log.events[special_columns["id_column"]] = log.events[special_columns["id_column"]].astype(float) 
        log.relations[special_columns["id_column"]] = log.relations[special_columns["id_column"]].astype(float) 
        log.events["Scope1"] = log.events[kwargs["scope_column"]]
        print("Scope examples: ")
        for i in range(5):
            print(log.events[kwargs["scope_column"]][i*5])
        
        sc_lvl = int(input("Select the scope level: ")) 

        
        for col in log.events.columns:
            if col not in special_columns.values():
                col_func_map[col] = dtype_to_func(col,type(log.events[col][0]))
            
            
        col_func_map[special_columns["id_column"]] = ["min", setify]
        col_func_map[special_columns["ts_column"]] = ['min','max']

        ###TODO: needs to be changed to scope
        col_func_map[special_columns["act_column"]] = lambda x: pd.Series.mode(x)[0] 

        log.events[kwargs["scope_column"]] = log.events[kwargs["scope_column"]].apply(truncate_lvl, level=sc_lvl)
        
        agg_events = log.events.groupby([kwargs["scope_column"],
            pd.Grouper(key=special_columns["ts_column"], freq='20h')],
            as_index=False).agg(col_func_map)


        new_columns = []
        for x in agg_events.columns:
            if x == (special_columns["ts_column"],'min'):
                new_columns.append(special_columns["ts_column"] + ':start')
            elif x == (special_columns["id_column"], 'setify'):
                new_columns.append("old_ids")
            else:
                new_columns.append(x[0])
        agg_events.columns = new_columns   
        agg_events.sort_values(special_columns["id_column"], inplace=True, ignore_index=True)

        #change relations eid column
        value_mapping = agg_events.apply(get_values_mapping, axis=1,
                        old_ids_column="old_ids", new_id_column=special_columns["id_column"])
        value_mapping = value_mapping.aggregate(concat_dicts)
        log.relations = map_ids(log.relations, special_columns["id_column"], value_mapping)
        
        log.events = agg_events.drop(columns="old_ids")

        #change relation columns besides id
        log.relations[log.event_activity] = log.relations[log.event_id_column]\
                                .map(log.events.set_index(log.event_id_column)[log.event_activity])
        log.relations[log.event_timestamp] = log.relations[log.event_id_column]\
                                .map(log.events.set_index(log.event_id_column)[log.event_timestamp])  
        log.relations.drop_duplicates(inplace=True)
        log.relations.reset_index(drop=True,inplace=True)
        print(log.events)
        print(log.relations)
        return log

def aggregate_objects(log, **kwargs):
    col_func_map = {}
    special_columns = {
            "id_column": "ocel:oid",
            }
    col_func_map[special_columns["id_column"]] = ["min", setify]

    for col in log.objects.columns:
            if col not in special_columns.values():
                col_func_map[col] = dtype_to_func(col,type(log.objects[col][0]))

    print("Scope examples: ")
    for i in range(5):
        print(log.objects[kwargs["scope_column"]][i*5 % len(log.objects)])

    sc_lvl = int(input("Select the scope level: ")) 
    agg_objs = log.objects[log.objects[kwargs["object_column"]] == kwargs["object_type"]]
  
    not_agg_objs = log.objects[log.objects[kwargs["object_column"]] != kwargs["object_type"]]
    agg_objs[kwargs["scope_column"]] = agg_objs[kwargs["scope_column"]].apply(truncate_lvl, level=sc_lvl)
    agg_objs = agg_objs.groupby([kwargs["scope_column"]],
            as_index=False).agg(col_func_map)
    print(agg_objs)
    
    # change oid in relations table
    value_mapping = agg_objs.apply(get_values_mapping, axis=1,
                    old_ids_column=(special_columns["id_column"],"setify"), new_id_column=(special_columns["id_column"],"min"))
    value_mapping = value_mapping.aggregate(concat_dicts)
    log.relations = map_ids(log.relations, special_columns["id_column"], value_mapping)

    agg_objs = agg_objs.drop(columns=(special_columns["id_column"],"setify"))
    agg_objs = agg_objs.droplevel(1, axis=1)
    agg_objs.sort_values(special_columns["id_column"], inplace=True, ignore_index=True)

    log.objects = pd.concat([agg_objs,not_agg_objs])

    log.relations.drop_duplicates(inplace=True)
    log.relations.reset_index(drop=True, inplace=True)

    print(log.objects)
    print(log.relations.head(30))

    return log

def execute_aggregation(log, **kwargs):
    
   
    if  kwargs["evt_or_obj"] == "e":
        agg_log = aggregate_events(log, **kwargs)
    elif kwargs["evt_or_obj"] == "o":
        agg_log = aggregate_objects(log, **kwargs)
        
    return agg_log



#________________________SELECTION FUNCTION___________________________    
    
def compare_paths(path1, path2):
        if re.search(path2,path1):
            return True
        else:
            return False

# "*" means any deepness of scope is allowed 
def selection_function(df: pd.DataFrame , scope_sep = "/", **kwargs):
    scope = df[kwargs["scope_column"]]
    regex = re.sub("\?"+ scope_sep,'((\\\w+|\\\s)+'+scope_sep+')?',kwargs["regex"])
    regex = re.sub("\*" + scope_sep,'(.*'+scope_sep+')*',regex)
    print(regex)
    paths = scope.apply(compare_paths, path2=(regex))
    paths = paths[paths] #Only where values True i.e. paths match
    return df.loc[paths.index]

def execute_selection(log, **kwargs):
    kwargs["regex"] = str(input("Specify regex: ")) 
    if kwargs["evt_or_obj"] == 'e':
        df = selection_function(log.events, **kwargs)
        log.events = df
    elif kwargs["evt_or_obj"] == 'o':
        grouped = log.objects.groupby(log.objects[kwargs["object_column"]])
        df = grouped.get_group(kwargs["object_type"])
        df = selection_function(df, **kwargs)
        log.objects = df
        # df = pd.DataFrame()
        # for name in log.objects[kwargs["object_column"]].unique():
        #     df2 = grouped.get_group(name)
        #     if name == kwargs["object_type"]:
        #         df2 = selection_function(df2, **kwargs)
        #     df = pd.concat([df,df2])
    
    return log


#_____________________________Relabeling________________________________
def get_scope_at_level(scope, lvl, sep="/"):
    split = tuple(scope.rsplit(sep))
    return split[min(len(split)-1,lvl)]

def relabel_function(df: pd.DataFrame, column:str, **kwargs):
    print("Scope examples: ")
    for i in range(5):
        print(df[kwargs["scope_column"]][i*5 % len(df)])
    sc_lvl = int(input("Select the scope level: ")) 
    df[column] = df[kwargs["scope_column"]].apply(get_scope_at_level, lvl = sc_lvl)
    return df


    

def execute_relabel(log, **kwargs):
    
    if kwargs["evt_or_obj"] == 'e':
        df = relabel_function(log.events, column="ocel:activity", **kwargs)
        log.events = df
    elif kwargs["evt_or_obj"] == 'o':
        df = log.objects[log.objects[kwargs["object_column"]] == kwargs["object_type"]]
        df = relabel_function(df, column=kwargs["object_column"], **kwargs)
        log.objects = df
    
    return log


#_____________________________START OF SCRIPT___________________________________________________

# filepath = str(input("Filepath: "))
filepath = "/Users/dzoba/Studies/MasterThesis/Preparation/toy_log2.jsonocel"
method =  str(input("Selection function (s), aggregation (a) or relabelling (r): "))
if method not in ["s","a","r","test"]:
    print("wrong method")
else:
    log = jsonocel.importer.apply(filepath)
    kwargs = {}
    kwargs["evt_or_obj"] = str(input("Should the action be performed on events (e) or objects (o)?: "))
    if kwargs["evt_or_obj"] == 'e':
        print(log.events.columns)
    elif kwargs["evt_or_obj"] == 'o':
        print(log.objects.columns)
        # object_column = str(input("Select the column specifyng the object type: "))
        kwargs["object_column"] = "ocel:type"
        print(log.objects[log.object_type_column].value_counts().to_dict())
        kwargs["object_type"] = str(input("Select the object type: "))
    kwargs["scope_column"] = str(input("Select scope column: ")) 

agg_log = pm4py.objects.ocel.obj.OCEL()
if method == "s":
    agg_log = execute_selection(log, **kwargs)
elif method == "a":
    agg_log = execute_aggregation(log, **kwargs)
elif method == 'r':
    agg_log = execute_relabel(log, **kwargs)
elif method =="test": 
    print(type(log.events["scope"]))
    print(truncate(log.events["scope"]))
