from flask import request, make_response, jsonify
from functools import wraps
import jwt
from pymysql import cursors
from Config_Database.config import app, conp

def token_required(f):
    @wraps(f)
    def decorator():
        token = None
        # pass jwt-token in headers
        if 'x-api-key' in request.headers:
            token = request.headers['x-api-key']
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "ກະລຸນາຢືນຢັນຕົວຕົນ ຫຼື session ຫມົດອາຍຸ"}), 401)
        try:
            cursor = conp.cursor(cursors.DictCursor)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = "SELECT username FROM useraccount WHERE public_id = %s"
            public_id=data['public_id']
            cursor.execute(current_user, public_id)
            d = cursor.fetchone()
            username = d['username']
            
        except:
            return make_response(jsonify({"message": "ຢືນຢັນຕົວຕົນຜິດພາດ ກະລຸນາຢືນຢັນຕົວຕົນໃຫມ່"}), 401)

        return f(username)
    return decorator