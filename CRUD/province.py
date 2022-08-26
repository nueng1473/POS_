from Config_Database.config import app, conp
from Error import error
from flask import jsonify, request
import pymysql
import re

@app.route('/register', methods =['POST'])
def register():
    msg = ''
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    if username and password and email and request.method == 'POST':
        cursor = conp.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            conp.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return msg

@app.route('/create_province', methods=['POST'])
def create_province():
    try:
        _json = request.json
        _province = _json['province']
        if _province and request.method == 'POST':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO province(province) VALUES(%s)"
            bindData = (_province)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Province added successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        print(e)

@app.route('/province', methods=['GET'])
def province():
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM province")
        provRows = cursor.fetchall()
        respone = jsonify(provRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

@app.route('/province/<int:prov_id>', methods=['GET'])
def province_details(prov_id):
    try:
        conn = conp
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT prov_ID, province FROM province WHERE prov_ID = %s", prov_id)
        provRow = cursor.fetchone()
        respone = jsonify(provRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

@app.route('/update_province', methods=['PUT'])
def update_province():
    try:
        _json = request.json
        _provID = _json['prov_ID']
        _province = _json['province']
        if _provID and _province and request.method == 'PUT':
            conn = conp
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE province SET province = %s WHERE prov_ID = %s"
            bindData = (_province, _provID)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Province updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return error.not_found()
    except Exception as e:
        print(e)

@app.route('/delete_province/<int:prov_id>', methods=['DELETE'])
def delete_province(prov_id):
    try:
        conn = conp
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM province WHERE prov_ID =%s", (prov_id,))
        conn.commit()
        respone = jsonify('Province deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)