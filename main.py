from Config_Database import config
from CRUD import employee, position, user, login, session, province, department, moving

if __name__ == '__main__':
    config.app.run(host='0.0.0.0', port=1000,threaded=True, debug=True)