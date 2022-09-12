from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from applying import Applying


app = Flask(__name__)
CORS(app)
api = Api(app)


class Employees(Resource):
    def get(self):
        return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]} 

class FileUpload(Resource):
    def get(self):
        return {"good": "nice"}

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(FileUpload, '/fileUpload')
api.add_resource(Applying, '/applying')

if __name__ == '__main__':
     app.run(port=5002)