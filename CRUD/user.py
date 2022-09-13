from Config_Database.config import app, conp, cursor
from flask import jsonify, request
from werkzeug.security import generate_password_hash
import uuid
from Authentication.Authentication import token_required
from Error.error import exist_data, server_error

@app.route('/create_user', methods=['POST'])
@token_required
def create_user(data):
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        passhash = generate_password_hash(_password)
        if passhash and _username:
            cursor.execute("SELECT username FROM useraccount WHERE username = %s", (_username))
            row = cursor.fetchone()
            if row:
                resp = jsonify({'message':'ມີຜູ້ໃຊ້ນີ້ແລ້ວ'}), 405
            else:
                public_id = (uuid.uuid4())
                sqlQuery = "INSERT INTO useraccount (username, password, public_id) VALUES (%s, %s, %s)"
                bindData = (_username, passhash, public_id)
                cursor.execute(sqlQuery, bindData)
                conp.commit()
                resp = jsonify({'message':'ເພີ່ມຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
            return resp
        else:
            resp = jsonify({'message': 'ກະລຸນາປ້ອນຂໍ້ມູນ'}), 403
            return resp
    except Exception:
        return server_error()

@app.route('/users', methods=['GET'])
@token_required
def user(data):
    try:
        cursor.execute("SELECT d1.username, d2.emp_name, d1.password, d3.pos_name \
            FROM useraccount as d1 inner join employee as d2 on (d1.username=d2.emp_ID) \
                inner join position as d3 on (d2.pos_ID=d3.pos_ID) WHERE d2.status = 2")
        userRows = cursor.fetchall()
        respone = jsonify(userRows), 200
        return respone
    except Exception:
        return server_error()

@app.route('/search_user', methods=['POST'])
@token_required
def user_details(data):
    try:
        _json = request.json
        id = _json['username']
        cursor.execute("SELECT d1.username, d2.emp_name, d1.password, d3.pos_name \
            FROM useraccount as d1 inner join employee as d2 on (d1.username=d2.emp_ID) \
                inner join position as d3 on (d2.pos_ID=d3.pos_ID) WHERE d2.status = 2 and username = %s", id)
        userRow = cursor.fetchall()
        respone = jsonify(userRow), 200
        return respone
    except Exception:
        return server_error()

@app.route('/update_user', methods=['PUT'])
@token_required
def update_user(data):
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        passhash = generate_password_hash(_password)
        if _username and passhash:
            sqlQuery = "UPDATE useraccount SET password = %s WHERE username = %s"
            bindData = (passhash, _username)
            cursor.execute(sqlQuery, bindData)
            conp.commit()
            respone = jsonify({'message': 'ອັດເດດຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
            return respone
        else:
            return exist_data()
    except Exception:
        return server_error()

@app.route('/delete_user', methods=['DELETE'])
@token_required
def delete_user(data):
    try:
        _json = request.json
        id = _json['username']
        cursor.execute("DELETE FROM useraccount WHERE username =%s", (id))
        conp.commit()
        respone = jsonify({'message': 'ລົບຂໍ້ມູນສຳເລັດ', 'status': 'ok'}), 201
        return respone
    except Exception:
        return server_error()