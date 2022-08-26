from Config_Database import config
from CRUD import province, prosition, department, employee, user, login, session

if __name__ == '__main__':
    config.app.run(host='0.0.0.0', port=1000,threaded=True, debug=True)