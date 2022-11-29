from flask_restful import Resource
from flask import request
import json
from utils import get_filepath_from_name


class EventLogs(Resource):
    def post(self, task):
        if task == 'import':
            file = request.files["log"]
            file.save(get_filepath_from_name(request.form['name']))
            return json.dumps({'result': 'ok'})
