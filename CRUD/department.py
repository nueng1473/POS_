from Config_Database.config import app, conp
from Error.error import not_found
from flask import jsonify, request
from pymysql import cursors
from re import match

@app.route('/create_department', methods=['POST'])
def create_department():
    try:
        msg = ''
        json = request.json
        dep_name = json['dep_name']
        dep_level = json['dep_level']
        if dep_name and dep_level and request.method == 'POST':
            cursor = conp.cursor(cursors.DictCursor)
            sqlQuery = "SELECT dep_name, dep_level FROM department WHERE dep_name = %s"
            bindData = (dep_name,)
            cursor.execute(sqlQuery, bindData)
            province = cursor.fetchone()
            if province:
                msg = 'ມີຂໍ້ມູນແລ້ວ'
            elif not match(r'[ກ-ຮ]+', dep_name):
                msg = 'ໃສ່ໄດ້ແຕ່ ກ-ຮ'
            elif not match(r'[0-9]+', dep_level):
                msg = 'ໃສໄດ້ແຕ່ 1-9'
            else:
                cursor.execute('INSERT INTO department(dep_name, dep_level) VALUES(%s, %s)', (dep_name, dep_level))
                conp.commit()
                msg = 'You have successfully department !'
            # respone = jsonify('Department added successfully!')
            # respone.status_code = 200
            # return respone
        elif request.method == 'POST':
            msg = 'Please fill!'
        return msg
    except Exception as e:
        return not_found()

@app.route('/department', methods=['GET'])
def department():
    try:
        cursor = conp.cursor(cursors.DictCursor)
        cursor.execute("SELECT dep_name, dep_create_date, dep_level FROM department")
        depRows = cursor.fetchall()
        respone = jsonify(depRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
        return not_found()

@app.route('/department/<int:dep_id>', methods=['GET'])
def department_details(dep_id):
    try:
        conn = conp
        cursor = conn.cursor(cursors.DictCursor)
        cursor.execute("SELECT * FROM department WHERE dep_ID = %s", dep_id)
        depRow = cursor.fetchone()
        respone = jsonify(depRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

@app.route('/update_department', methods=['PUT'])
def update_department():
    try:
        _json = request.json
        _dep_ID = _json['dep_ID']
        _dep_name = _json['dep_name']
        _dep_level = _json['dep_level']
        if _dep_ID and _dep_name and _dep_level and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(cursors.DictCursor)
            sqlQuery = "UPDATE department SET dep_name = %s, dep_level = %s WHERE dep_ID = %s"
            bindData = (_dep_name, _dep_level, _dep_ID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Department updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)

@app.route('/delete_department/<string:dep_id>', methods=['DELETE'])
def delete_department(dep_id):
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM department WHERE dep_ID =%s", (dep_id,))
        conn.commit()
        respone = jsonify('Department deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)