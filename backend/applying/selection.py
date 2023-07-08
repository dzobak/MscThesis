import re
import pandas as pd


def compare_paths(path1, path2):
    if pd.isnull(path1):
        return True
    if re.search(path2, path1):
        return True
    else:
        return False


def selection_function(df: pd.DataFrame, scope_sep='/', **kwargs):
    scope = df[kwargs['scope_column']]
    regex = re.sub('\?' + scope_sep, '((\\\w+|\\\s)+' +
                   scope_sep+')?', kwargs['regex'])
    # '*' means any deepness of scope is allowed
    regex = re.sub('\*' + scope_sep, '(.*'+scope_sep+')*', regex)
    paths = scope.apply(compare_paths, path2=(regex))
    paths = paths[paths]  # Only where values True i.e. paths match
    return df.loc[paths.index]


def execute_selection(log, **kwargs):

    if kwargs['is_event_transformation']:
        # kwargs['regex'] = str(input('Specify regex: '))
        log.events = selection_function(log.events, **kwargs)
        log.relations = log.relations[log.relations[log.event_id_column].isin(
            set(log.events[log.event_id_column]))]
        log.objects = log.objects[log.objects[log.object_id_column].isin(
            set(log.relations[log.object_id_column]))]
        # log.relations.drop(rows_to_drop, inplace=True)

    elif kwargs['is_object_transformation']:
        # df = log.objects[log.objects[log.object_type_column]
        #                  == kwargs['object_type']]           
        df = selection_function(log.objects, **kwargs)
        log.objects = df
        log.relations = log.relations[log.relations[log.object_id_column].isin(
            set(log.objects[log.object_id_column]))]
        log.events = log.events[log.events[log.event_id_column].isin(
            set(log.relations[log.event_id_column]))]
    return log
