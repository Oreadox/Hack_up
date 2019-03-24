# encoding: utf-8

from app import api, app
from app.api.User import SingUp



# api.add_resource(login, '/api/login/')
api.add_resource(SingUp, '/api/user/signup/')

if __name__ == '__main__':
    app.run(debug=True)
