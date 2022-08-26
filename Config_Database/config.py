from flask import Flask
from flask_cors import CORS
from flaskext.mysql import MySQL
from sshtunnel import SSHTunnelForwarder
import pymysql
from datetime import timedelta
app = Flask(__name__)
CORS(app)
mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
# app.config['MYSQL_DATABASE_DB'] = 'test'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
tunnel = SSHTunnelForwarder(('54.179.29.104', 22), ssh_password="123456Aa!", ssh_username="ubuntu",remote_bind_address=("127.0.0.1", 3306))
tunnel.start()
conp = pymysql.connect(host='127.0.0.1', user="root", passwd="123456Aa!", database="test", port=tunnel.local_bind_port)
mysql.init_app(app)