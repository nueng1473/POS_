from Config_Database import config
from Error import error
from flask import jsonify, request
import pymysql

@config.app.route('/create_position', methods=['POST'])
def create_position():
    try:
        _json = request.json
        _pos_name = _json['pos_name']
        if _pos_name and request.method == 'POST':
            conn = config.conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO test.position(pos_name) VALUES(%s)"
            bindData = (_pos_name)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Position added successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        print(e)

@config.app.route('/position', methods=['GET'])
def position():
    try:
        conn = config.conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM test.position")
        posRows = cursor.fetchall()
        respone = jsonify(posRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

@config.app.route('/position/<string:pos_id>', methods=['GET'])
def position_details(pos_id):
    try:
        conn = config.conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT pos_ID, pos_name FROM test.position WHERE pos_ID = %s", pos_id)
        posRow = cursor.fetchone()
        respone = jsonify(posRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

@config.app.route('/update_position', methods=['PUT'])
def update_position():
    try:
        _json = request.json
        _pos_ID = _json['pos_ID']
        _pos_name = _json['pos_name']
        if _pos_ID and _pos_name and request.method == 'PUT':
            conn = config.conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE test.position SET pos_name = %s WHERE pos_ID = %s"
            bindData = (_pos_name, _pos_ID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Position updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        print(e)

@config.app.route('/delete_position/<string:pos_id>', methods=['DELETE'])
def delete_position(pos_id):
    try:
        conn = config.conp
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test.position WHERE pos_ID =%s", (pos_id,))
        conn.commit()
        respone = jsonify('Position deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)