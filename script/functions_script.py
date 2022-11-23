import pm4py
from pm4py.objects.ocel.importer.jsonocel import importer
from pm4py.objects.ocel.exporter.jsonocel import exporter
import os

import pandas as pd
from aggregation import *
from selection import *
from relabelling import *

# _____________________________START OF SCRIPT___________________________________________________
while(True):
    try:
        if filename:
            samelog = True if str(input('Use last log (y/n)?: ')) == 'y' else False
    except NameError:
        filename = None      
    if not filename or not samelog:
        print("Logs_available:")
        print(os.listdir(os.path.join('.', 'logs'm1)))
        filename = str(input('Specify filename: '))
        # filepath = '/Users/dzoba/Studies/MasterThesis/Preparation/toy_log2.jsonocel'
        filepath = os.path.join('.', 'logs', filename + '.jsonocel')
        log = importer.apply(filepath)
        print(log.get_extended_table())
    else:
        log = agg_log
    method = str(
        input('Selection function (s), aggregation (a) or relabelling (r): '))
    if method not in ['s', 'a', 'r', 'test']:
        raise Exception('No correct method selected')
    else:
        kwargs = {}
        evt_or_obj = str(
            input('Should the action be performed on events (e) or objects (o)?: '))
        kwargs['is_event_transformation'] = True if evt_or_obj == 'e' else False
        kwargs['is_object_transformation'] = True if evt_or_obj == 'o' else False
        if kwargs['is_event_transformation']:
            print(log.events.columns)
        elif kwargs['is_object_transformation']:

            # object_column = str(input('Select the column specifyng the object type: '))
            kwargs['object_column'] = 'ocel:type'
            print(log.objects[log.object_type_column].value_counts().to_dict())
            kwargs['object_type'] = str(input('Select the object type: '))
            print(log.objects.columns)
        else:
            raise Exception('Objects or Events have to be selected')
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

    print(agg_log.get_extended_table())
    filename = str(input('Save under filename: '))
    exporter.apply(agg_log, os.path.join('.', 'logs', filename + '.jsonocel'))
