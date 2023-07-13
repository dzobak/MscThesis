from flask_restful import Resource
from flask import send_file
from utils import get_image_filepath_from_name, get_alt_image_filepath_from_name


class Images(Resource):

    def get(self, filename):
        try:
            return send_file(get_image_filepath_from_name(filename), mimetype='image/png')
        except:
             return send_file(get_alt_image_filepath_from_name(filename), mimetype='image/png')
        
    # TODO: scope images dont get deleted when log is deleted.
