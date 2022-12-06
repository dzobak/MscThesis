from flask_restful import Resource
from flask import request
import json
from utils import get_filepath_from_name
from OCEL_extended import OCEL_ext
from pm4py.objects.ocel.importer.jsonocel import importer as ocel_import


class EventLogs(Resource):
    def post(self, task):
        if task == 'import':
            file = request.files["log"]
            file.save(get_filepath_from_name(request.form['name']))
            return json.dumps({'result': 'ok'})
        elif task == 'details':
            data = request.get_json()
            print(data['eventlog'])
            if data['eventlog'] == 'toy_log3':
                print('here')
                log = OCEL_ext(ocel_import.apply(
                    get_filepath_from_name(data['eventlog']),parameters={'param:event:activity': 'scope:ocel:activity'}))
            else:
                log = OCEL_ext(ocel_import.apply(
                    get_filepath_from_name(data['eventlog'])))

            return json.dumps(log.get_dict_summary())
