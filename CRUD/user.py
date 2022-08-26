from Config_Database import config
from Error import error
from flask import jsonify, request
import pymysql
from werkzeug.security import generate_password_hash

# user_table
@config.app.route('/create_user', methods=['POST'])
def create_user():
    try:
        _json = request.json
        _emp_id = _json['username']
        _password = _json['password']
        _user_type = _json['user_type']
        passhash = generate_password_hash(_password)
        print(passhash)
        if passhash and _user_type and _emp_id and request.method == 'POST':
            conn = config.conp.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO test.useraccount (password, user_type, username) VALUES (%s, %s, %s)"
            bindData = (passhash, _user_type, _emp_id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        print(e)


@config.app.route('/user', methods=['GET'])
def user():
    try:
        conn = config.conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT username, password, user_type FROM useraccount")
        userRows = cursor.fetchall()
        respone = jsonify(userRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@config.app.route('/users/<string:user_id>', methods=['GET'])
def user_details(user_id):
    try:
        conn = config.conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM test.useraccount WHERE username = %s", user_id)
        userRow = cursor.fetchone()
        respone = jsonify(userRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@config.app.route('/update_user', methods=['PUT'])
def update_user():
    try:
        _json = request.json
        _emp_id = _json['username']
        _password = _json['password']
        _user_type = _json['user_type']
        passhash = generate_password_hash(_password)
        if _emp_id and passhash and _user_type and request.method == 'PUT':
            conn = config.conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE test.useraccount SET password = %s, user_type = %s WHERE username = %s"
            bindData = (passhash, _user_type, _emp_id)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        print(e)

@config.app.route('/delete_user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = config.conp
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test.useraccount WHERE username =%s", (user_id,))
        conn.commit()
        respone = jsonify('User deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)