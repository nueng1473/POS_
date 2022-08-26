from Config_Database import config
from flask import jsonify, request

@config.app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@config.app.errorhandler(405)
def have_data(error=None):
    message = {
        'status': 405,
        'message': 'have data ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 405
    return resp

@config.app.errorhandler(500)
def server_error(error=None):
    message = {
        'status': 500,
        'message': 'have data? or server error: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp

@config.app.errorhandler(400)
def username_error(error=None):
    message = {
        'status': 400,
        'message': 'Username ຫຼື Password ບໍ່ຖືກຕ້ອງ',
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp