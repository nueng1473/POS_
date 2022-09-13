import imp
from CRUD.position import position_name
from CRUD.session import session
from Config_Database.config import app, conp
from flask import jsonify, request
from pymysql import cursors
from re import match
from Error.error import server_error
from Authentication.Authentication import token_required
from CRUD.department import department_name
@app.route('/moving_detail', methods=['GET'])
@token_required
def moving_detail(data):
    try:
        conn = conp
        cursor = conn.cursor(cursors.DictCursor)
        cursor.execute("SELECT  d2.emp_name, d2.emp_surname, d3.dep_name,\
             d4.session_name, d5.pos_name, d1.description, d1.moving_date, d6.dep_name, d7.session_name, d8.pos_name \
            FROM moving as d1 inner join employee as d2 on (d1.emp_ID = d2.emp_ID) \
                inner join department as d3 on (d1.dep_ID = d3.dep_ID) \
                    inner join session as d4 on (d1.session_ID = d4.session_ID) \
                        inner join position as d5 on (d1.pos_ID = d5.pos_ID) \
                            inner join department as d6 on (d2.dep_ID = d6.dep_ID) \
                                inner join session as d7 on (d2.session_ID = d7.session_ID) \
                                    inner join position as d8 on (d2.pos_ID = d8.pos_ID) WHERE d2.status = 2")
        provRows = cursor.fetchall()
        respone = jsonify(provRows), 200
        return respone
    except Exception as e:
        print(e)

@app.route('/moving', methods=['POST'])
@token_required
def moving(data):
    try:
        _json = request.json
        emp_ID = _json['emp_ID']
        dep_name = _json['dep_name']
        pos_name = _json['pos_name']
        session_name = _json['session_name']
        cursor = conp.cursor(cursors.DictCursor)
        dep = department_name(dep_name)
        pos = position_name(pos_name)
        ses = session(session_name)
        cursor.execute('SELECT emp_ID, pos_ID, dep_ID, session_ID FROM employee WHERE emp_ID = %s', (emp_ID, ))
        empid = cursor.fetchone()
        depid = empid['dep_ID']
        sessionid = empid['session_ID']
        posid = empid['pos_ID']
        cursor.execute('INSERT INTO moving (dep_ID, session_ID, pos_ID, emp_ID) \
            VALUES (%s, %s, %s, %s)', (depid, sessionid, posid, emp_ID))
        cursor.execute('UPDATE employee  SET pos_ID = %s, session_ID = %s, dep_ID = %s, \
                        status = 2 WHERE (emp_ID = %s)', (pos, ses, dep, emp_ID))
        conp.commit()
        respone = jsonify({'message': 'ຍ້າຍຂໍ້ມູນສຳເລັດ', 'status':'ok'}), 201
        return respone

    except Exception as e:
        print(e)