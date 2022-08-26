from flask import request
from Config_Database import config

class Province():
        _json = request.json
        _provID = _json['prov_ID']
        _province = _json['province']
