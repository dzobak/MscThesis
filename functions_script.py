# Python imports
import os
import re
from pathlib import Path

# Library imports
import pandas as pd
import pm4py


def get_scope_tuple(scope):
    # For aggregation and relabelling
    return tuple(scope.rsplit('/'))


def is_unique(s: pd.Series):
    # For aggregation, checks if all the values provided in the series are the same
    a = s.to_numpy()
    return (a[0] == a).all()


def truncate_lvl(scope_value, level):
    scope_tuple = get_scope_tuple(scope_value)
    truncated_scope = '/'.join(scope_tuple[:level + 1])
    return truncated_scope


def truncate(series):
    # After truncating, all scopes will be the same, so a representative is picked
    first_scope = series.iloc[0]

    tuple_series = series.apply(get_scope_tuple)
    scope_df = pd.DataFrame(tuple_series.to_list())

    # Holds the value until which scope level the scope should be truncated
    scope_equality_lvl = -1
    for i in range(len(scope_df.columns)):
        if not is_unique(scope_df[i]):
            scope_equality_lvl = i - 1
            break
        elif i == len(scope_df.columns) - 1:
            scope_equality_lvl = i

    truncated_scope = truncate_lvl(first_scope, scope_equality_lvl)

    return truncated_scope


def dtype_to_func(col, dtype):
    # For Aggregation
    if re.search(r"scope", col, re.IGNORECASE):
        return truncate
    elif isinstance(dtype, str):
        return 'mode'
    elif isinstance(dtype, int) or isinstance(dtype, float):
        return 'sum'


def aggregation(log, **kwargs):
    col_func_map = {}
    is_event = kwargs["evt_or_obj"] == "e"
    if is_event:
        special_columns = {
            "id_column": "ocel:eid",
            "ts_column": "ocel:timestamp",
            "act_column": "ocel:activity",
            "sc_column": kwargs["scope_column"]
        }

        log.events[special_columns["id_column"]] = log.events[special_columns["id_column"]].astype(
            float)
        log.events["Scope1"] = log.events[special_columns["sc_column"]]

        print("Scope examples: ")
        for i in range(5):
            print(log.events[special_columns["sc_column"]][i * 5])

        sc_lvl = int(input("Select the scope level: "))

        for col in log.events.columns:
            if col not in special_columns.values():
                col_func_map[col] = dtype_to_func(col, type(log.events[col][0]))

        col_func_map[special_columns["id_column"]] = "min"
        col_func_map[special_columns["ts_column"]] = ['min', 'max']
        col_func_map[special_columns["act_column"]] = lambda val: pd.Series.mode(val)[0]

        log.events[special_columns["sc_column"]] = log.events[special_columns["sc_column"]].apply(
            truncate_lvl, level=sc_lvl)

        agg_log = log.events.groupby([special_columns["sc_column"],
                                      pd.Grouper(key=special_columns["ts_column"], freq='20h')],
                                     as_index=False).agg(col_func_map)

        new_columns = []
        for x in agg_log.columns:
            if x == (special_columns["ts_column"], 'min'):
                new_columns.append(special_columns["ts_column"] + ':start')
            else:
                new_columns.append(x[0])
        agg_log.columns = new_columns
        agg_log.sort_values(special_columns["id_column"], inplace=True, ignore_index=True)

        print(agg_log)
        print(agg_log.columns)
    else:
        raise NotImplementedError("TODO implement aggregation for objects")


# ________________________SELECTION FUNCTION___________________________
def compare_paths(path1, path2):
    if re.search(path2, path1):
        return True
    else:
        return False


def selection_function(df: pd.DataFrame, scope_sep="/", **kwargs):
    # "*" means any deepness of scope is allowed
    scope = df[kwargs["scope_column"]]
    regex = re.sub("\?" + scope_sep, '((\\\w+|\\\s)+' + scope_sep + ')?', kwargs["regex"])
    regex = re.sub("\*" + scope_sep, '(.*' + scope_sep + ')*', regex)
    print(regex)
    paths = scope.apply(compare_paths, path2=regex)
    paths = paths[paths]  # Only where values True i.e. paths match
    return df.loc[paths.index]


def execute_selection(log, **kwargs):
    kwargs["regex"] = str(input("Specify regex: "))
    is_event = kwargs["evt_or_obj"] == "e"
    if is_event:
        df = selection_function(log.events, **kwargs)
    else:
        grouped = log.objects.groupby(log.objects[kwargs["object_column"]])
        df = grouped.get_group(kwargs["object_type"])
        df = selection_function(df, **kwargs)
        # df = pd.DataFrame()
        # for name in log.objects[kwargs["object_column"]].unique():
        #     df2 = grouped.get_group(name)
        #     if name == kwargs["object_type"]:
        #         df2 = selection_function(df2, **kwargs)
        #     df = pd.concat([df,df2])
    print(df)


# _____________________________Relabeling________________________________
def get_scope_at_level(scope, lvl, sep="/"):
    split = tuple(scope.rsplit(sep))
    return split[min(len(split) - 1, lvl)]


def relabel_function(df: pd.DataFrame, column: str, **kwargs):
    print("Scope examples: ")
    for i in range(5):
        print(df[kwargs["scope_column"]][i * 5 % len(df)])
    sc_lvl = int(input("Select the scope level: "))
    df[column] = df[kwargs["scope_column"]].apply(get_scope_at_level, lvl=sc_lvl)
    return df


def execute_relabel(log, **kwargs):
    is_event = kwargs["evt_or_obj"] == "e"
    relabel_column = "ocel:activity" if is_event else kwargs["object_column"]
    df = relabel_function(log.objects, column=relabel_column, **kwargs)
    print(df)


def read_eventlog():
    base_path = Path(os.getcwd())
    file_path = base_path / "backend/event_logs/toy_log2.jsonocel"
    return pm4py.read_ocel(str(file_path))


# _____________________________START OF SCRIPT___________________________________________________

def main():
    log = read_eventlog()
    method = str(input("Selection function (s), aggregation (a) or relabelling (r): "))

    if method not in ["s", "a", "r", "test"]:
        print("wrong method")
    else:
        kwargs = {
            "evt_or_obj": str(
                input("Should the action be performed on events (e) or objects (o)?: "))
        }
        if kwargs["evt_or_obj"] == 'e':
            print(log.events.columns)
        elif kwargs["evt_or_obj"] == 'o':
            print(log.objects.columns)
            # object_column = str(input("Select the column specifying the object type: "))
            kwargs["object_column"] = "ocel:type"
            print(log.objects[log.object_type_column].value_counts().to_dict())
            kwargs["object_type"] = str(input("Select the object type: "))
        kwargs["scope_column"] = str(input("Select scope column: "))

        if method == "s":
            execute_selection(log, **kwargs)
        elif method == "a":
            aggregation(log, **kwargs)
        elif method == 'r':
            execute_relabel(log, **kwargs)
        elif method == "test":
            print(type(log.events["scope"]))
            print(truncate(log.events["scope"]))

if __name__ == '__main__':
    main()
