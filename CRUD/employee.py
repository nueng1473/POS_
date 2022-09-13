from CRUD.department import department_name
from CRUD.position import position_name
from CRUD.province import province_name
from CRUD.session import session_name
from Config_Database.config import app, conp, cursor
from flask import jsonify, request
from re import match
import os
from werkzeug.utils import secure_filename
from Authentication.Authentication import token_required
from Error.error import server_error

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/employees', methods=['GET'])
@token_required
def emp(data):
    try:
        cursor.execute("SELECT d1.emp_ID, d1.gender, d1.emp_name, d1.emp_surname,\
             d1.emp_tel, d1.village, d1.district, d1.profilepic, d4.province, d3.dep_name, d5.session_name, d2.pos_name\
              from employee as d1 inner join position as d2 on (d1.pos_ID=d2.pos_ID)\
                inner join department as d3 on(d1.dep_ID=d3.dep_ID) \
                inner join province as d4 on(d1.prov_ID=d4.prov_ID) \
                    inner join session as d5 on (d1.session_ID = d5.session_ID) WHERE d1.status = 2")
        empRows = cursor.fetchall()
        respone = jsonify(empRows), 200
        return respone
    except Exception:
        return server_error()

@app.route('/create_employee', methods=['POST'])
@token_required
def create_emp(data):
    try:
        _form = request.form
        _emp_ID = _form['emp_ID']
        _name = _form['emp_name']
        _surname = _form['emp_surname']
        _tel = _form['emp_tel']
        _village = _form['village']
        _district = _form['district']
        _pos_name = _form['pos_name']
        _dep_name = _form['dep_name']
        _prov_name = _form['province']
        _session_name = _form['session_name']
        _gender = _form['gender']
        _status = 2
        file = request.files['file']
        if _emp_ID and _name and _surname and _tel and _village and _district \
            and _pos_name and _dep_name and _session_name and _gender and file:
            cursor.execute('SELECT emp_ID FROM employee WHERE emp_ID = %s', (_emp_ID))
            empid = cursor.fetchone()
            if empid:
                respone = jsonify({'message': 'ມີລະຫັດນີ້ແລ້ວ'}), 405
            elif not match(r'[A-Z]+[0-9]+', _emp_ID):
                respone = jsonify({'message': 'ຮູບແບບລະຫັດບໍ່ຖືກຕ້ອງ'}), 403
            elif file and (not allowed_file(file.filename)):
                respone = jsonify({'message': 'ຮູບບໍ່ຖືກຕ້ອງ'}), 403
            else:
                _dep = department_name(_dep_name)
                _pos = position_name(_pos_name)
                _ses = session_name(_session_name)
                _prov = province_name(_prov_name)
                filename = secure_filename(file.filename)
                filesave = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filesave)
                sqlQuery = "INSERT INTO employee(emp_ID, emp_name, emp_surname, \
                    gender, emp_tel, village, district, pos_ID, dep_ID, prov_ID, session_ID, status, profilepic) \
                        VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                bindData = (_emp_ID, _name, _surname, _gender, _tel, _village,
                            _district, _pos, _dep, _prov, _ses, _status, "http://47.250.49.41/static/uploads/"+filename)
                cursor.execute(sqlQuery, bindData)
                conp.commit()
                respone = jsonify({'message': 'ເພີ່ມຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
            return respone
        else:
            respone  =  jsonify({'message': 'ກະລຸນາໃສ່ຂໍ້ມູນໃຫ້ຄົບຖ້ວນ'}), 403
            return respone
    except Exception:
        return server_error()

@app.route('/search_employee', methods=['POST'])
@token_required
def emp_details(data):
    try:
        _json = request.json
        _emp_ID = _json['emp_ID']
        _name = _json['emp_name']
        if _emp_ID or _name:
            cursor.execute('SELECT emp_ID, emp_name FROM employee WHERE (emp_ID LIKE %s or emp_name LIKE %s) and status = 2', (_emp_ID, _name))
            empid = cursor.fetchall()
            if not empid:
                respone = jsonify({'message': 'ບໍ່ມີຂໍ້ມູນ'}), 404
            else:
                cursor.execute("SELECT d1.emp_ID, d1.gender, d1.emp_name, d1.emp_surname, \
                    d1.village, d1.district, d1.profilepic, d4.province, d5.session_name,d3.dep_name, d2.pos_name\
                    from employee as d1 inner join position as d2 on (d1.pos_ID=d2.pos_ID)\
                        inner join department as d3 on(d1.dep_ID=d3.dep_ID) \
                        inner join province as d4 on(d1.prov_ID=d4.prov_ID) \
                            inner join session as d5 on(d1.session_ID = d5.session_ID) WHERE\
                            ( d1.emp_ID LIKE %s or d1.emp_name LIKE %s ) and d1.status = 2", (_emp_ID, _name))
                empRow = cursor.fetchall()
                respone = jsonify(empRow), 200
            return respone
    except Exception:
        return server_error()

@app.route('/update_employee', methods=['PUT'])
@token_required
def update_emp(data):
    try:
        _form = request.form
        _emp_ID = _form['emp_ID']
        
        _name = _form['emp_name']
        _surname = _form['emp_surname']
        _tel = _form['emp_tel']
        _village = _form['village']
        _district = _form['district']
        _pos_name = _form['pos_name']
        _dep_name = _form['dep_name']
        _prov_name = _form['province']
        _session_name = _form['session_name']
        _gender = _form['gender']
        file = request.files['file']
        print(_form)
        print(file)
        if _name and _surname and _tel and _village and _district and\
             _pos_name and _dep_name and _prov_name and _session_name and _gender and file:
            if file and (not allowed_file(file.filename)):
                respone = jsonify({'message': 'ຮູບບໍ່ຖືກຕ້ອງ'}), 403
            else:
                _dep = department_name(_dep_name)
                _pos = position_name(_pos_name)
                _ses = session_name(_session_name)
                _prov = province_name(_prov_name)
                filename = secure_filename(file.filename)
                filesave = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(filename)
                file.save(filesave)
                sqlQuery = "UPDATE employee  SET emp_name = %s, emp_surname = %s, gender = %s, \
                    emp_tel = %s, village = %s, district = %s, pos_ID = %s, session_ID = %s, dep_ID = %s, \
                        prov_ID = %s, status = 2, profilepic = %s  WHERE (emp_ID = %s)"
                bindData = (_name, _surname, _gender, _tel, _village,
                            _district, _pos, _ses, _dep, _prov, "http://47.250.49.41/static/uploads/"+filename, _emp_ID)
                cursor.execute(sqlQuery, bindData)
                conp.commit()
                respone = jsonify({'message': 'ອັບເດດຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
        else:
            respone = jsonify({'message': 'ກະລຸນາໃສ່ຂໍ້ມູນໃຫ້ຄົບຖ້ວນ'}), 403
        return respone
    except Exception:
        return server_error()

@app.route('/delete_employee', methods=['DELETE'])
@token_required
def delete_emp(data):
    try:
        _json = request.json
        _emp_ID = _json['emp_ID']
        cursor.execute("UPDATE employee  SET status = 1 WHERE (emp_ID = %s)", (_emp_ID))
        conp.commit()
        respone = jsonify({'message': 'ລົບຂໍ້ມູນສຳເລັດ', 'status': 'ok'}), 200
        return respone
    except Exception:
        return server_error()