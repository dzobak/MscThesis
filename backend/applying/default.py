from flask_restful import Resource
import pm4py
import pandas as pd
from OCEL_extended import OCEL_ext
from pm4py.objects.ocel.importer.jsonocel import importer as ocel_import
from pm4py.objects.ocel.exporter.jsonocel import exporter as ocel_export
import json
from flask import request
from applying.selection import execute_selection
from applying.aggregation import execute_aggregation
from applying.relabelling import execute_relabelling
from utils import get_max_scope_depth, get_filepath_from_name, get_name_from_filepath, get_file_folder, get_column_functions
from glob import glob


class Applying(Resource):
    def get(self, task):
        if task in ['default', 'names']:
            folder = get_file_folder()
            filepaths = glob(folder+'*.jsonocel')
            event_log_names = [get_name_from_filepath(filepath)
                               for filepath in filepaths]
            if task == 'default':
                event_logs = []
                for name in event_log_names:
                    event_log = OCEL_ext(ocel_import.apply(
                        get_filepath_from_name(name)))
                    events, objects = pm4py.objects.ocel.exporter.util.clean_dataframes\
                        .get_dataframes_from_ocel(event_log)

                    # TODO:make a list for scope columns
                    event_logs.append({
                        'value': name,
                        # need to change that to actual scope columns
                        'e_scopes': event_log.event_scope_columns,
                        'e_columns': [col for col in events.columns],
                        # need to change that to actual scope columns
                        'o_scopes': [scope for scope in objects.columns if 'scope' in scope],
                        'o_columns': [col for col in objects.columns]
                    })
                return event_logs
            elif task == 'names':
                return event_log_names
        elif 'eventLog' in task:
            name = task.split('eventLog', maxsplit=1)[1]
            event_log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(name)))
            return event_log.events.head(10).to_json(orient='records')
        elif 'objects' in task:
            name = task.split('objects', maxsplit=1)[1]
            event_log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(name)))
            return event_log.objects.head(10).to_json(orient='records')
        elif 'logdata' in task:
            name = task.split('logdata', maxsplit=1)[1]
            print('***************')
            print(name)
            event_log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(name)))
            events, objects = pm4py.objects.ocel.exporter.util.clean_dataframes\
                .get_dataframes_from_ocel(event_log)

            logdata = {
                'value': name,
                # need to change that to actual scope columns
                'e_scopes': event_log.event_scope_columns,
                'e_columns': [col for col in events.columns],
                # need to change that to actual scope columns
                'o_scopes': [scope for scope in objects.columns if 'scope' in scope],
                'o_columns': [col for col in objects.columns]
            }
            print(logdata)
            return json.dumps(logdata)
        else:
            return {
                'good': 'niddce',
                'hithere': task
            }

    def post(self, task):
        if task == 'regex':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(get_filepath_from_name(
                data['eventlogname'])))
            filtered_log = execute_selection(log, **data)
            # sel = Selection()
            # filtered_log = sel.selection_function(
            #     regex=data['regex'], df=log, scope_column=data['scope'])
            ocel_export.apply(filtered_log, get_filepath_from_name(
                data['newlogname']))
            if data['is_event_transformation']:
                return filtered_log.events.head(10).to_json(orient='records')
            elif data['is_object_transformation']:
                return filtered_log.objects.head(10).to_json(orient='records')
        elif task == 'scopelevel':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlog'])))
            df = log.events if data["is_event_transformation"] else log.objects
            max_scope_depth = get_max_scope_depth(df[data["scope_column"]])
            return json.dumps({'levels': list(range(max_scope_depth))})
        elif task == 'aggregation':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlogname'])))
            aggregated_log = execute_aggregation(log, **data)
            ocel_export.apply(aggregated_log, get_filepath_from_name(
                data['newlogname']))
            if data['is_event_transformation']:
                return aggregated_log.events.head(10).to_json(orient='records')
            elif data['is_object_transformation']:
                return aggregated_log.objects.head(10).to_json(orient='records')
        elif task == 'aggregation_functions':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlogname'])))

            return json.dumps(get_column_functions(log, **data))
        elif task == 'relabel':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlogname'])))
            relabeled_log = execute_relabelling(log, **data)
            ocel_export.apply(relabeled_log, get_filepath_from_name(
                data['newlogname']))
            if data['is_event_transformation']:
                return relabeled_log.events.head(10).to_json(orient='records')
            elif data['is_object_transformation']:
                return relabeled_log.objects.head(10).to_json(orient='records')
        else:
            return {
                'good': 'niddce',
                'hithere': task
            }
