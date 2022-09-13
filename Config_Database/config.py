from flask import Flask, url_for, redirect
from flask_cors import CORS
from flaskext.mysql import MySQL
from sshtunnel import SSHTunnelForwarder
from pymysql import cursors, connect
from datetime import timedelta
app = Flask(__name__)
CORS(app)
mysql = MySQL()
UPLOAD_FOLDER = 'Config_Database/static/uploads/'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
# app.config['MYSQL_DATABASE_DB'] = 'test'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
tunnel = SSHTunnelForwarder(('52.220.74.160', 22), ssh_password="123456Aa!", ssh_username="ubuntu",remote_bind_address=("127.0.0.1", 3306))
tunnel.start()
conp = connect(host='127.0.0.1', user="root", passwd="123456Aa!", database="pos", port=tunnel.local_bind_port)
mysql.init_app(app)
cursor = conp.cursor(cursors.DictCursor)
@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('Config_Database', filename='static/uploads/' + filename))