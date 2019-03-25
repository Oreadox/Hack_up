# encoding: utf-8

from app import api, app
from app.api.authentication import SingUp, Login, ChangePassword, DeleteAccount, ForgetPassword, \
    UserConfirm, ResetPassword

api.add_resource(Login, '/api/user/login/')
api.add_resource(SingUp, '/api/user/signup/')
api.add_resource(ChangePassword, '/api/user/change/')
api.add_resource(ForgetPassword, '/api/user/forget/')
api.add_resource(ResetPassword, '/api/user/reset/')
api.add_resource(UserConfirm, '/api/user/confirm/')
api.add_resource(DeleteAccount, '/api/user/delete/')

if __name__ == '__main__':
    app.run(debug=True)

