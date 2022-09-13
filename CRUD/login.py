from Config_Database.config import app, conp
from flask import jsonify, request, session
from werkzeug.security import check_password_hash
from pymysql import cursors
from re import match
import jwt

@app.route('/login', methods=['POST'])
def login():
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        if _username and _password:
            cursor = conp.cursor(cursors.DictCursor)
            sql = "SELECT d1.username, d1.password, d1.public_id, d2.status FROM useraccount as d1\
                 inner join employee as d2 on (d1.username=d2.emp_ID)  WHERE d1.username=%s and d2.status = 2"
            sql_where = (_username,)
            cursor.execute(sql, sql_where)
            row = cursor.fetchone()
            username = row['username']
            password = row['password']
            public_id = row['public_id']
            if row:
                if not match(r'[A-Z0-9]+', _username):
                    return jsonify({'message': 'username ຫຼື password ບໍ່ຖືກຕ້ອງ'}), 401
                if check_password_hash(password, _password):
                    token = jwt.encode({'public_id': public_id}, app.config['SECRET_KEY'], 'HS256')
                    session['username'] = username
                    conn = conp
                    cursor = conn.cursor(cursors.DictCursor)
                    cursor.execute("SELECT d1.emp_ID, d5.password, d1.gender, d1.emp_name, d1.emp_surname,\
                        d1.emp_tel, d1.village, d1.district, d1.profilepic, d4.province, d3.dep_name, d2.pos_name\
                        from employee as d1 inner join position as d2 on (d1.pos_ID=d2.pos_ID)\
                        inner join department as d3 on(d1.dep_ID=d3.dep_ID) \
                        inner join province as d4 on(d1.prov_ID=d4.prov_ID)\
                        inner join useraccount as d5 on(d1.emp_ID=d5.username) WHERE d1.emp_ID = %s and d1.status = 2", (username))
                    userRows = cursor.fetchone()
                    return jsonify({'message': 'ເຂົ້າສູ່ລະບົບສຳເລັດ', 'token':token, "expiresIn": 60000, 'status': 'ok', 'user': userRows}), 200
                else:
                    return jsonify({'message': 'username ຫຼື password ບໍ່ຖືກຕ້ອງ'}), 401
        else:
            resp = jsonify({'message': 'ກະລຸນາປ້ອນ username ແລະ password'}), 403
            return resp
    except Exception:
        return jsonify({'message': 'username ຫຼື password ບໍ່ຖືກຕ້ອງ'}), 401



@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'ອອກຈາກລະບົບສຳເລັດ', 'status': 'ok'}), 200
