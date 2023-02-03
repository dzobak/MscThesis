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
from utils import *
from glob import glob


class Applying(Resource):
    parameters={'param:event:activity': 'scope:ocel:activity'}

    def get(self, task):
        if task in ['default', 'names']:
            folder = get_file_folder()
            filepaths = glob(folder+'*.jsonocel')
            event_log_names = [get_name_from_filepath(filepath)
                               for filepath in filepaths]
            if task == 'default':
                event_logs = []
                for name in event_log_names:
                    #TODO error here if ocel file contains no data 
                    event_log = OCEL_ext(ocel_import.apply(
                        get_filepath_from_name(name), parameters=self.parameters))
                    # events, objects = pm4py.objects.ocel.exporter.util.clean_dataframes\
                    #     .get_dataframes_from_ocel(event_log)

                    # TODO:make a list for scope columns
                    event_logs.append({
                        'value': name,
                        # need to change that to actual scope columns
                        'e_scopes': event_log.event_scope_columns,
                        'e_columns': [col for col in event_log.events.columns],
                        # need to change that to actual scope columns
                        'o_scopes': event_log.object_scope_columns,
                        'o_columns': [col for col in event_log.objects.columns]
                    })
                return event_logs
            elif task == 'names':
                return event_log_names
        elif 'eventLog' in task:
            name = task.split('eventLog', maxsplit=1)[1]
            event_log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(name), parameters=self.parameters))
            return event_log.get_readable_timestamp().events.head(20).to_json(orient='records')
        elif 'objects' in task:
            name = task.split('objects', maxsplit=1)[1]
            event_log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(name), parameters=self.parameters))
            return event_log.objects.head(10).to_json(orient='records')
        elif 'logdata' in task:
            name = task.split('logdata', maxsplit=1)[1]
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(name), parameters=self.parameters))

            logdata = {
                'value': name,
                # need to change that to actual scope columns
                'e_scopes': log.event_scope_columns,
                'e_columns': [col for col in log.events.columns],
                # need to change that to actual scope columns
                'o_scopes': log.object_scope_columns,
                'o_columns': [col for col in log.objects.columns]
            }
  
            return json.dumps(logdata)
        elif 'delete' in task:
            name = task.split('delete', maxsplit=1)[1]
            delete_file(name)
        else:
            return {
                'good': 'niddce',
                'hithere': task
            }

    def post(self, task):
        if task == 'regex':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(get_filepath_from_name(
                data['eventlogname']), parameters=self.parameters))
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
                get_filepath_from_name(data['eventlog']), parameters=self.parameters))
            df = log.events if data["is_event_transformation"] else log.objects
            max_scope_depth = get_max_scope_depth(df[data["scope_column"]])
            return json.dumps({'levels': list(range(max_scope_depth))})
        elif task == 'aggregation':
            # TODO Aggregation fails if done a second time on the log
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlogname']), parameters=self.parameters))
            aggregated_log, new_to_old_id_mapping = execute_aggregation(log, **data)
            ocel_export.apply(aggregated_log, get_filepath_from_name(
                data['newlogname']))
            # if data['is_event_transformation']:
            #     return aggregated_log.events.head(10).to_json(orient='records')
            # elif data['is_object_transformation']:
            #     return aggregated_log.objects.head(10).to_json(orient='records')
            return json.dumps({'eventlogname': data['eventlogname'],'mapping': new_to_old_id_mapping})
        elif task == 'aggregation_functions':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlogname']), parameters=self.parameters))

            return json.dumps(get_column_function_options(log, **data))
        elif task == 'relabel':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlogname']), parameters=self.parameters))
            relabeled_log = execute_relabelling(log, **data)
            ocel_export.apply(relabeled_log, get_filepath_from_name(
                data['newlogname']))
            if data['is_event_transformation']:
                return relabeled_log.events.head(10).to_json(orient='records')
            elif data['is_object_transformation']:
                return relabeled_log.objects.head(10).to_json(orient='records')
        elif task == 'oldrows':
            data = request.get_json()
            log = OCEL_ext(ocel_import.apply(
                get_filepath_from_name(data['eventlogname']), parameters=self.parameters))
            data['rows_index'] = [str(id) for id in data['rows_index']]
            # print(data['rows_index'][0])
            # print(log.events[log.event_id_column])
            if data['is_event_transformation']:
                return log.events[log.events[log.event_id_column].isin(data['rows_index'])].to_json(orient='records')
            elif data['is_object_transformation']:
                return log.objects.loc[[data['rows_index']]].to_json(orient='records')

            
        elif task == 'save':
            data = request.get_json()
            rename_file(data['old_name'], data['new_name'])
        else:
            return {
                'good': 'niddce',
                'hithere': task
            }
