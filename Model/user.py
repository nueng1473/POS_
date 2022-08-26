from flask import request
from Config_Database import config

class User(config.mysql.Model):
    _json = request.json
    _emp_id = _json['username']
    _password = _json['password']
    _user_type = _json['user_type']