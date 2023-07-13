from flask import Flask, render_template, send_from_directory
from flask_restful import Api
from flask_cors import CORS

from applying.default import Applying
from event_logs.event_logs import EventLogs
from images import Images

app = Flask(__name__)
CORS(app)
api = Api(app)

 
api.add_resource(EventLogs, '/eventlogs/<task>', '/static/static/logs/<task>')
api.add_resource(Applying, '/applying/<task>')
api.add_resource(Images, '/images/<filename>')

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
     return send_from_directory('./static', path)  

@app.route('/', methods=['GET'])
@app.route('/logs')
@app.route('/applying')
def root():
     return render_template('index.html', static_folder='static')




if __name__ == '__main__':
     app.run(port=5002, threaded=True)