from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from applying.default import Applying
from event_logs.event_logs import EventLogs
from images import Images

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(EventLogs, '/eventlogs/<task>')
api.add_resource(Applying, '/applying/<task>')
api.add_resource(Images, '/images/<filename>')

if __name__ == '__main__':
     app.run(port=5002)