from Config_Database.config import app, conp
from Error.error import not_found
from flask import jsonify, request
from pymysql import cursors
from re import match

@app.route('/oraganization', methods = ['GET'])
def oraganization():
    try:
        # _json = request.json
        # _org_no = _json['org_plan_no']
        # _emp_ID = _json['emp_ID']
        # _session_ID = _json['session_ID']
        cursor = conp.cursor(cursors.DictCursor)
        cursor.execute("SELECT d1.org_plan_no, d2.emp_name, d4.province, d3.dep_name \
            from oraganization as d1 \
            inner join employee as d2 on (d1.emp_ID=d2.emp_ID) \
            inner join department as d3 on(d2.dep_ID=d3.dep_ID) \
            inner join province as d4 on(d2.prov_ID=d4.prov_ID)")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception:
        pass