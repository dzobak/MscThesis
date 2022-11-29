from flask_restful import Resource
from flask import request
import json
from utils import get_filepath


class EventLogs(Resource):
    def post(self, task):
        if task == 'import':
            file = request.files["log"]
            file.save(get_filepath(request.form['name']))
            return json.dumps({'result': 'ok'})
