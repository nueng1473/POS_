from Config_Database.config import app, conp
from Error.error import server_error
from flask import jsonify, request
from pymysql import cursors
from re import match
from Authentication.Authentication import token_required

@app.route('/create_form', methods=['POST'])
@token_required
def create_form(data):
    try:
        _json = request.json
        _header = _json['head_name']
        _emp_ID = _json['emp_ID']
        _title1 = _json['title_1']
        _title2 = _json['title_2']
        if _header and _emp_ID and _title1 and _title2:
            cursor = conp.cursor(cursors.DictCursor)
            cursor.execute('SELECT head_name FROM header_form WHERE head_name = %s', (_header))
            form = cursor.fetchone()
            if form:
                respone = jsonify({'message': 'ມີແບບຟອມນີ້ແລ້ວ'})
                respone.status_code = 400
            else:
                sqlQuery = "INSERT INTO header_form (head_name, emp_ID) VALUES (%s, %s)"
                bindData = (_header, _emp_ID)
                cursor.execute(sqlQuery, bindData)
                conp.commit()
                sql = "INSERT INTO title_form (title_1, title_2, head_ID) VALUES (%s, %s, %s)"
                data_form = (_title1, _title2, _header)
                cursor.execute(sql, data_form)
                conp.commit()
                respone = jsonify({'message':'ສາ້ງແບບຟອມສຳເລັດ', 'status':'ok'})
                respone.status_code = 200
            return respone
        else:
            return server_error()
    except Exception:
        return server_error()


@app.route('/form', methods=['GET'])
@token_required
def form(data):
    try:
        conn = conp
        cursor = conn.cursor(cursors.DictCursor)
        cursor.execute("SELECT head_name, title_1, title_2, date_create \
            FROM header_form as d1 inner join title_form as d2 on (d1.head_ID = d2.head_ID)")
        userRows = cursor.fetchall()
        respone = jsonify(userRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)