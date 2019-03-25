# encoding: utf-8

from app import api, app
from app.api.authentication import SingUp, Login, ChangePassword, DeleteAccount, ForgetPassword, UserConfirm

api.add_resource(Login, '/api/user/login/')
api.add_resource(SingUp, '/api/user/signup/')
api.add_resource(ChangePassword, '/api/user/change_password/')
api.add_resource(ForgetPassword, '/api/user/ForgetPassword/')
api.add_resource(UserConfirm, '/api/user/UserConfirm/')
api.add_resource(DeleteAccount, '/api/user/delete_account/')

if __name__ == '__main__':
    app.run(debug=True)

