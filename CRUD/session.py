import re
from Config_Database.config import app, conp
from Error import error
from flask import jsonify, request
import pymysql

@app.route('/session', methods=['GET'])
def session():
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM session")
        provRows = cursor.fetchall()
        respone = jsonify(provRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

@app.route('/create_session', methods=['POST'])
def create_session():
    
    try:
        _json = request.json
        _name = _json['session_name']
        res = re.sub(r'[^a-zA-Zກ-ຮ]', '', _name)
        for ch in _name:
            if ch.isalpha():
                res += ch
        if res == "" and request.method == 'POST':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO session(session_name) VALUES(%s)"
            bindData = (res)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('session added successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        return error.have_data()


@app.route('/update_session', methods=['PUT'])
def update_session():
    try:
        _json = request.json
        _ID = _json['session_ID']
        _name = _json['session_name']
        if _ID and _name and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE session SET session_name = %s, WHERE session_ID = %s"
            bindData = (_name, _ID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('ses updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        print(e)

# @app.route('/delete_department/<string:dep_id>', methods=['DELETE'])
# def delete_department(dep_id):
#     try:
#         conn = conp
#         cursor = conn.cursor()
#         cursor.execute(
#             "DELETE FROM department WHERE dep_ID =%s", (dep_id,))
#         conn.commit()
#         respone = jsonify('Department deleted successfully!')
#         respone.status_code = 200
#         return respone
#     except Exception as e:
#         print(e)