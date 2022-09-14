from flask_restful import Resource
import pm4py
import pandas as pd
import re
from pm4py.objects.ocel.importer.jsonocel import importer as ocel_import
import os

event_log_names = ["toy_log2", "running-example"]
# event_log = ocel_import.apply(os.path.join(".","event_logs","toy_log2"+".jsonocel"))



class Applying(Resource):
    def get(self, method):
        if method == "default":
            event_logs=[]
            for name in event_log_names:
                event_log = ocel_import.apply(os.path.join
                    (".","event_logs",name+".jsonocel"))
                events, objects = pm4py.objects.ocel.exporter.util.clean_dataframes.get_dataframes_from_ocel(event_log)
                scopes = [scope for scope in events.columns if "scope" in scope]
                event_logs.append({"value":name, "scopes":scopes})
            return event_logs
        elif  "eventLog" in method:
            return {"good": method.split("eventLog", maxsplit=1)[1]}
        else:
            return {
                "good": "niddce",
                "hithere": method
            }

    