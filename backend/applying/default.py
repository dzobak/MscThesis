from flask_restful import Resource
import pm4py
import pandas as pd
import re
from pm4py.objects.ocel.importer.jsonocel import importer as ocel_import


event_log = ocel_import.apply("./event_logs/toy_log2.jsonocel")

events, objects = pm4py.objects.ocel.exporter.util.clean_dataframes.get_dataframes_from_ocel(event_log)

class Applying(Resource):
    def get(self, method):
        if method == "default":
            scopes = [scope for scope in events.columns if "scope" in scope]
            print(events.columns)
            return {
                "event_logs" : ["toy_log2", "running_example"],
                "scopes": scopes,
            }
        else:
            return {
                "good": "niddce",
                "hithere": method
            }

    