from flask_restful import Resource
import pm4py
import pandas as pd
import re

class Applying(Resource):
    def get(self):
        return {"good": "niddce"}