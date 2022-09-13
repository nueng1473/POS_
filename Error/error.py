from Config_Database import config
from flask import jsonify, request

# @config.app.errorhandler(200)
# def success(error=None):
#     message = {
#         'status': 200,
#         'message': 'ການຮ້ອງຂໍຂອງທ່ານສຳເລັດແລ້ວ: ' + request.url,
#     }
#     resp = jsonify(message)
#     resp.status_code = 200
#     return resp

# @config.app.errorhandler(201)
# def data(error=None):
#     message = {
#         'status': 201,
#         'message': 'ການເພີ່ມຂໍ້ມູນຂອງທ່ານສຳເລັດແລ້ວ: ' + request.url,
#     }
#     resp = jsonify(message)
#     resp.status_code = 201
#     return resp

@config.app.errorhandler(400)
def Bad_Request(error=None):
    message = {
        'status': 400,
        'message': 'ຄຳຂໍຮ້ອງຂອງທ່ານຜິດພາດ: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp

@config.app.errorhandler(401)
def UnAuthorized(error=None):
    message = {
        'status': 401,
        'message': 'ກະລຸນາຢືນຢັນບັນຊີຂອງທ່ານ: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 401
    return resp

@config.app.errorhandler(403)
def exist_data(error=None):
    message = {
        'status': 403,
        'message': 'ຜິດພາດທີ່: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403
    return resp

@config.app.errorhandler(413)
def file_to_large(error=None):
    message = {
        'status': 413,
        'message': 'ກະລູນາກວດສອບຂະໜາດຟາຍຮູບຂອງທ່ານ: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 413
    return resp

@config.app.errorhandler(500)
def server_error(error=None):
    message = {
        'status': 500,
        'message': 'ເກີດຂໍ້ຜິດພາດທີ່ເຊີເວີ: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp