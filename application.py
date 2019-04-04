# encoding: utf-8

from app import api, app, socketio
from app.config import use_web

if use_web:
    # web端(默认运行）
    from app.api.web.user import UserData, Email, ForgetPassword, Token, Password
    from app.api.web.room import RoomData, Join
    from app.api.web.socket import RoomData as socket

    api.add_resource(UserData, '/api/user/current')
    api.add_resource(Email, '/api/user/email')
    api.add_resource(ForgetPassword, '/api/user/forget/')
    api.add_resource(Token, '/api/user/token')
    api.add_resource(Password, '/api/user/password')
    api.add_resource(RoomData, '/api/room/data')
    api.add_resource(Join, '/api/room/join')
    socketio.on_namespace(socket())
else:
    # 微信小程序
    from app.api.wechat.authentication import Login, ReName

    api.add_resource(Login, '/api/user/login/')
    api.add_resource(ReName, '/api/user/rename/')

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, host='0.0.0.0', port=80)
