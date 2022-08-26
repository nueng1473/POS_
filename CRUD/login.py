from Error.error import username_error
from Config_Database.config import app, conp
from flask import jsonify, request, session
from werkzeug.security import check_password_hash
from pymysql import cursors
from re import match

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return jsonify({'message': 'You are already logged in', 'username': username})
    else:
        resp = jsonify({'message': 'Unauthorized'})
        resp.status_code = 401
        return resp

@app.route('/login', methods=['POST'])
def login():
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        if _username and _password:
            cursor = conp.cursor(cursors.DictCursor)
            sql = "SELECT username, password FROM useraccount WHERE username=%s"
            sql_where = (_username,)
            cursor.execute(sql, sql_where)
            row = cursor.fetchone()
            username = row['username']
            password = row['password']
            if row:
                if not match(r'[A-Z0-9]+', _username):
                    resp = jsonify({'message': 'Username error'})
                    resp.status_code = 400
                    return resp
                elif check_password_hash(password, _password):
                    session['username'] = username
                    conn = conp
                    cursor = conn.cursor(cursors.DictCursor)
                    cursor.execute("SELECT username, password FROM useraccount")
                    userRows = cursor.fetchone()
                    return jsonify({'message': 'You are logged in successfully', 'status': 'ok','user': userRows})
                else:
                    resp = jsonify({'message': 'Bad Request - invalid password'})
                    resp.status_code = 400
                    return resp
        else:
            resp = jsonify({'message': 'Bad Request - invalid credendtials'})
            resp.status_code = 400
            return resp
    except Exception:
        return username_error()

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'You successfully logged out'})