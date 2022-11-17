import pm4py
from pm4py.objects.ocel.importer import jsonocel

import pandas as pd
from aggregation import *
from selection import *
from relabelling import *

# _____________________________START OF SCRIPT___________________________________________________

# filepath = str(input('Filepath: '))
filepath = '/Users/dzoba/Studies/MasterThesis/Preparation/toy_log2.jsonocel'
method = str(
    input('Selection function (s), aggregation (a) or relabelling (r): '))
if method not in ['s', 'a', 'r', 'test']:
    print('wrong method')
else:
    log = jsonocel.importer.apply(filepath)
    kwargs = {}
    kwargs['evt_or_obj'] = str(
        input('Should the action be performed on events (e) or objects (o)?: '))
    if kwargs['evt_or_obj'] == 'e':
        print(log.events.columns)
    elif kwargs['evt_or_obj'] == 'o':
        print(log.objects.columns)
        # object_column = str(input('Select the column specifyng the object type: '))
        kwargs['object_column'] = 'ocel:type'
        print(log.objects[log.object_type_column].value_counts().to_dict())
        kwargs['object_type'] = str(input('Select the object type: '))
    kwargs['scope_column'] = str(input('Select scope column: '))

agg_log = pm4py.objects.ocel.obj.OCEL()
if method == 's':
    agg_log = execute_selection(log, **kwargs)
elif method == 'a':
    agg_log = execute_aggregation(log, **kwargs)
elif method == 'r':
    agg_log = execute_relabel(log, **kwargs)
elif method == 'test':
    print(type(log.events['scope']))
    print(truncate(log.events['scope']))
