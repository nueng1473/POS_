from Authentication.Authentication import token_required
from Config_Database.config import app, conp, cursor
from Error.error import server_error
from flask import jsonify

# @app.route('/create_province', methods=['POST'])
# def create_province():
#     try:
#         _json = request.json
#         _province = _json['province']
#         if _province and request.method == 'POST':
#             sqlQuery = "INSERT INTO province(province) VALUES(%s)"
#             bindData = (_province)
#             cursor.execute(sqlQuery, bindData)
#             conp.commit()
#             respone = jsonify('Province added successfully!')
#             respone.status_code = 200
#             return respone
#         else:
#             return server_error()
#     except Exception as e:
#         print(e)

@app.route('/province', methods=['GET'])
@token_required
def province_detail(data):
    try:
        cursor.execute("SELECT prov_ID, province FROM province")
        provRows = cursor.fetchall()
        respone = jsonify(provRows)
        respone.status_code = 200
        return respone
    except Exception:
        return server_error()

def province_name(data):
    cursor.execute('SELECT prov_ID FROM province WHERE province = %s', (data, ))
    prov = cursor.fetchone()
    prov = prov['prov_ID']
    return prov

# @app.route('/province/<int:prov_id>', methods=['GET'])
# def province_details(prov_id):
#     try:
#         conn = conp
#         cursor = conn.cursor(cursors.DictCursor)
#         cursor.execute("SELECT prov_ID, province FROM province WHERE prov_ID = %s", prov_id)
#         provRow = cursor.fetchone()
#         respone = jsonify(provRow)
#         respone.status_code = 200
#         return respone
#     except Exception as e:
#         print(e)

# @app.route('/update_province', methods=['PUT'])
# def update_province():
#     try:
#         _json = request.json
#         _provID = _json['prov_ID']
#         _province = _json['province']
#         if _provID and _province and request.method == 'PUT':
#             conn = conp
#             cursor = conn.cursor(cursors.DictCursor)
#             sqlQuery = "UPDATE province SET province = %s WHERE prov_ID = %s"
#             bindData = (_province, _provID)
#             cursor.execute(sqlQuery, bindData)
#             conn.commit()
#             respone = jsonify('Province updated successfully!')
#             respone.status_code = 200
#             return respone
#         else:
#             return server_error()
#     except Exception as e:
#         print(e)

# @app.route('/delete_province/<int:prov_id>', methods=['DELETE'])
# def delete_province(prov_id):
#     try:
#         conn = conp
#         cursor = conn.cursor()
#         cursor.execute(
#             "DELETE FROM province WHERE prov_ID =%s", (prov_id,))
#         conn.commit()
#         respone = jsonify('Province deleted successfully!')
#         respone.status_code = 200
#         return respone
#     except Exception as e:
#         print(e)