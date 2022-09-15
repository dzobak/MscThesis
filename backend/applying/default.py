from flask_restful import Resource
import pm4py
import pandas as pd
import re
from pm4py.objects.ocel.importer.jsonocel import importer as ocel_import
import os
import json
from flask import request
from applying.selection import Selection 

event_log_names = ["toy_log2", "running-example"]
# event_log = ocel_import.apply(os.path.join(".","event_logs","toy_log2"+".jsonocel"))



class Applying(Resource):
    def get_path(self,name:str):
        return os.path.join(".","event_logs",name+".jsonocel")

    def get(self, task):
        if task == "default":
            event_logs=[]
            for name in event_log_names:
                event_log = ocel_import.apply(self.get_path(name))
                events, objects = pm4py.objects.ocel.exporter.util.clean_dataframes.get_dataframes_from_ocel(event_log)
                scopes = [scope for scope in events.columns if "scope" in scope]
                event_logs.append({"value":name, "scopes":scopes})
            return event_logs
        elif  "eventLog" in task:
            name = task.split("eventLog", maxsplit=1)[1]
            event_log = ocel_import.apply(self.get_path(name))
            return event_log.get_extended_table().head(10).to_json(orient="records")
        else:
            return {
                "good": "niddce",
                "hithere": task
            }

    def post(self, task):
        if task == "regex":
            data = request.get_json()
            print(data)
            print(type(data))
            log = ocel_import.apply(self.get_path(data["eventlog"])).get_extended_table()
            sel = Selection()
            filtered_log = sel.selection_function(regex=data["regex"], df=log
            ,scope_column=data["scope"])
            return json.dumps(filtered_log.head(10).to_json(orient="records"))
        else:
            return {
                "good": "niddce",
                "hithere": task
            }