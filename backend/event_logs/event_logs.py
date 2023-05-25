from flask_restful import Resource
from flask import request, send_file
import json
from utils import get_log_filepath_from_name, delete_file
from OCEL_extended import OCEL_ext
from pm4py.objects.ocel.importer.jsonocel import importer as ocel_import


class EventLogs(Resource):
    
    def delete(self,task):
        delete_file(task)

    def get(self,task):
        return send_file(get_log_filepath_from_name(task))

    def post(self, task):
        if task == 'import':
            file = request.files["log"]
            file.save(get_log_filepath_from_name(request.form['name']))
            return json.dumps({'result': 'ok'})
        elif task == 'details':
            data = request.get_json()
            #TODO this just works with my log
            if 'log' in data['eventlog']:
                log = OCEL_ext(ocel_import.apply(
                    get_log_filepath_from_name(data['eventlog']),parameters={'param:event:activity': 'ocel:scope:activity'}))
            else:
                log = OCEL_ext(ocel_import.apply(
                    get_log_filepath_from_name(data['eventlog'])))

            return json.dumps(log.get_dict_summary())
