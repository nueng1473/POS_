from Config_Database.config import app, conp, cursor
from flask import jsonify, request
from pymysql import cursors
from Authentication.Authentication import token_required
from Error.error import server_error

@app.route('/create_department', methods=['POST'])
@token_required
def create_department(data):
    try:
        json = request.json
        dep_name = json['dep_name']
        if dep_name:
            sqlQuery = "SELECT dep_name FROM department WHERE dep_name = %s"
            bindData = (dep_name)
            cursor.execute(sqlQuery, bindData)
            row = cursor.fetchone()
            if row:
                respone = jsonify({'message': 'ມີຂໍ້ມູນແລ້ວ'}), 405
            else:
                cursor.execute('INSERT INTO department(dep_name) VALUES(%s)', (dep_name, ))
                conp.commit()
                respone = jsonify({'message':'ເພີ່ມຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
            return respone
        else:
            respone = jsonify({'message':'ຂໍ້ມູນບໍ່ຄົບຖ້ວນ'}), 405
        return respone
    except Exception:
        return server_error()

@app.route('/departments', methods=['GET'])
@token_required
def department(data):
    try:
        cursor.execute("SELECT dep_ID, dep_name, dep_create_date FROM department")
        depRows = cursor.fetchall()
        respone = jsonify(depRows), 200
        return respone
    except Exception:
        return server_error()

@app.route('/search_department', methods=['POST'])
@token_required
def department_details(data):
    try:
        json = request.json
        name = json['dep_name']
        if name:
            cursor.execute("SELECT dep_name FROM department WHERE dep_name = %s", name)
            depRow = cursor.fetchall()
            if not depRow:
                respone = jsonify({'message': 'ບໍ່ມີຂໍ້ມູນ'}), 404
            else:
                cursor.execute("SELECT dep_name, dep_create_date FROM department WHERE dep_name = %s", name)
                depRow = cursor.fetchall()
                respone = jsonify(depRow), 200
            return respone
        else:
            return department()
    except Exception:
        return server_error()

@app.route('/update_department', methods=['PUT'])
@token_required
def update_department(data):
    try:
        _json = request.json
        _dep_ID = _json['dep_ID']
        _dep_name = _json['dep_name']
        if _dep_ID and _dep_name:
            sqlQuery = "UPDATE department SET dep_name = %s WHERE dep_ID = %s"
            bindData = (_dep_name, _dep_ID)
            cursor.execute(sqlQuery, bindData)
            conp.commit()
            respone = jsonify({'message': 'ອັດເດດຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
        else:
            respone = jsonify({'message': 'ກະລຸນາໃສ່ຂໍ້ມູນໃຫ້ຄົບຖ້ວນ'}), 403
        return respone
    except Exception:
        return server_error()

@app.route('/delete_department', methods=['DELETE'])
@token_required
def delete_department(data):
    try:
        _json = request.json
        _dep_name = _json['dep_name']
        cursor.execute("DELETE FROM department WHERE dep_name =%s", _dep_name)
        conp.commit()
        respone = jsonify({'message': 'ລົບຂໍ້ມູນສຳເລັດ', 'status': 'ok'}), 201
        return respone
    except Exception:
        respone = jsonify({'message':'ຂໍ້ມູນມີການໃຊ້ງານບໍ່ສາມາດລົບໄດ້'}), 403
        return respone

def department_name(data):
    cursor.execute('SELECT dep_ID FROM department WHERE dep_name = %s', (data, ))
    dep = cursor.fetchone()
    dep = dep['dep_ID']
    return dep