from Config_Database.config import app, conp, cursor
from Error.error import server_error
from flask import jsonify, request
from Authentication.Authentication import token_required

@app.route('/create_position', methods=['POST'])
@token_required
def create_position(data):
    try:
        json = request.json
        name = json['pos_name']
        if name:
            sqlQuery = "SELECT pos_name FROM position WHERE pos_name = %s"
            bindData = (name)
            cursor.execute(sqlQuery, bindData)
            row = cursor.fetchone()
            if row:
                respone = jsonify({'message': 'ມີຂໍ້ມູນແລ້ວ'}), 405
            else:
                cursor.execute("INSERT INTO position (pos_name) VALUES (%s)", (name))
                conp.commit()
                respone = jsonify({'message':'ເພີ່ມຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
            return respone
        else:
            respone = jsonify({'message':'ຂໍ້ມູນບໍ່ຄົບຖ້ວນ'}), 403
        return respone
    except Exception:
        return server_error()

@app.route('/positions', methods=['GET'])
@token_required
def position(data):
    try:
        cursor.execute("SELECT pos_ID, pos_name FROM position")
        posRows = cursor.fetchall()
        respone = jsonify(posRows), 200
        return respone
    except Exception:
        return server_error()

@app.route('/search_position', methods=['POST'])
@token_required
def position_details(data):
    try:
        json = request.json
        name = json['pos_name']
        if name:
            cursor.execute("SELECT pos_name FROM position WHERE pos_name = %s", name)
            depRow = cursor.fetchone()
            if not depRow:
                respone = jsonify({'message': 'ບໍ່ມີຂໍ້ມູນ'}), 404
            else:
                cursor.execute("SELECT pos_ID, pos_name FROM position WHERE pos_name = %s", name)
                depRow = cursor.fetchall()
                respone = jsonify(depRow), 200
            return respone
        else:
            return position()
    except Exception:
        return server_error()

@app.route('/update_position', methods=['PUT'])
@token_required
def update_position(data):
    try:
        _json = request.json
        _pos_ID = _json['pos_ID']
        _pos_name = _json['pos_name']
        if _pos_ID and _pos_name:
            sqlQuery = "UPDATE position SET pos_name = %s WHERE pos_ID = %s"
            bindData = (_pos_name, _pos_ID)
            cursor.execute(sqlQuery, bindData)
            conp.commit()
            respone = jsonify({'message': 'ອັດເດດຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
            return respone
        else:
            return jsonify({'message': 'ກະລຸນາໃສ່ຂໍ້ມູນໃຫ້ຄົບຖ້ວນ'}), 403
    except Exception:
        return server_error()

@app.route('/delete_position', methods=['DELETE'])
@token_required
def delete_position(data):
    try:
        _json = request.json
        name = _json['pos_name']
        cursor.execute("DELETE FROM position WHERE pos_name =%s", name)
        conp.commit()
        respone = jsonify({'message': 'ລົບຂໍ້ມູນສຳເລັດ', 'status': 'ok'}), 201
        return respone
    except Exception:
        respone = jsonify({'message':'ຂໍ້ມູນມີການໃຊ້ງານບໍ່ສາມາດລົບໄດ້'}), 403
        return respone

def position_name(data):
    cursor.execute('SELECT pos_ID FROM position WHERE pos_name = %s', (data, ))
    pos = cursor.fetchone()
    pos = pos['pos_ID']
    return pos
