from Config_Database.config import app, conp, cursor
from flask import jsonify, request
from Authentication.Authentication import token_required
from Error.error import server_error

@app.route('/create_session', methods=['POST'])
@token_required
def create_session(data):
    try:
        json = request.json
        dep_name = json['session_name']
        if dep_name:
            sqlQuery = "SELECT session_name FROM session WHERE session_name = %s"
            bindData = (dep_name)
            cursor.execute(sqlQuery, bindData)
            row = cursor.fetchone()
            if row:
                respone = jsonify({'message': 'ມີຂໍ້ມູນແລ້ວ'}), 405
            else:
                cursor.execute('INSERT INTO session (session_name) VALUES(%s)', (dep_name, ))
                conp.commit()
                respone = jsonify({'message':'ເພີ່ມຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
            return respone
        else:
            respone = jsonify({'message':'ຂໍ້ມູນບໍ່ຄົບຖ້ວນ'}), 403
        return respone
    except Exception:
        return server_error()

@app.route('/sessions', methods=['GET'])
@token_required
def session(data):
    try:
        cursor.execute("SELECT session_ID, session_name, session_create_date FROM session")
        depRows = cursor.fetchall()
        respone = jsonify(depRows), 200
        return respone
    except Exception:
        return server_error()

@app.route('/search_session', methods=['POST'])
@token_required
def session_details(data):
    try:
        json = request.json
        name = json['session_name']
        if name:
            cursor.execute("SELECT session_name FROM session WHERE session_name = %s", name)
            depRow = cursor.fetchone()
            if not depRow:
                respone = jsonify({'message': 'ບໍ່ມີຂໍ້ມູນ'}), 404
            else:
                cursor.execute("SELECT session_ID, session_name, session_create_date FROM session WHERE session_name = %s", name)
                depRow = cursor.fetchall()
                respone = jsonify(depRow), 200
            return respone
        else:
            return session()
    except Exception:
        return server_error()

@app.route('/update_session', methods=['PUT'])
@token_required
def update_session(data):
    try:
        _json = request.json
        _dep_ID = _json['session_ID']
        _dep_name = _json['session_name']
        if _dep_ID and _dep_name:
            sqlQuery = "UPDATE session SET session_name = %s WHERE session_ID = %s"
            bindData = (_dep_name, _dep_ID)
            cursor.execute(sqlQuery, bindData)
            conp.commit()
            respone = jsonify({'message': 'ອັດເດດຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
        else:
            respone = jsonify({'message': 'ກະລຸນາໃສ່ຂໍ້ມູນໃຫ້ຄົບຖ້ວນ'}), 403
        return respone
    except Exception:
        return server_error()

@app.route('/delete_session', methods=['DELETE'])
@token_required
def delete_session(data):
    try:
        _json = request.json
        _dep_name = _json['session_name']
        cursor.execute("DELETE FROM session WHERE session_name =%s", _dep_name)
        conp.commit()
        respone = jsonify({'message': 'ລົບຂໍ້ມູນສຳເລັດ', 'status': 'ok'}), 201
        return respone
    except Exception:
        respone = jsonify({'message':'ຂໍ້ມູນມີການໃຊ້ງານບໍ່ສາມາດລົບໄດ້'}), 403
        return respone

def session_name(data):
    cursor.execute('SELECT session_ID FROM session WHERE session_name = %s', (data, ))
    ses = cursor.fetchone()
    ses = ses['session_ID']
    return ses