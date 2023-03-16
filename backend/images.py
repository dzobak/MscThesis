from flask_restful import Resource
from flask import send_file
from utils import get_image_filepath_from_name


class Images(Resource):

    def get(self, filename):
        return send_file(get_image_filepath_from_name(filename), mimetype='image/png')
