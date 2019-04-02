# encoding: utf-8

from app import api, app, socketio
from app.config import use_web

if use_web:
    # web端(默认运行）
    from app.api.web.authentication import SingUp, Login, ChangePassword, DeleteAccount, ForgetPassword, \
        UserConfirm, ResetPassword
    from app.api.web.room import SetUp, Join, ChangeRoomPassword, Leave, Status, GetRoom, ChangeNotice
    from app.api.web.socket import RoomData

    api.add_resource(Login, '/api/user/login/')
    api.add_resource(SingUp, '/api/user/signup/')
    api.add_resource(ChangePassword, '/api/user/change/')
    api.add_resource(ForgetPassword, '/api/user/forget/')
    api.add_resource(ResetPassword, '/api/user/reset/')
    api.add_resource(UserConfirm, '/api/user/confirm/')
    api.add_resource(DeleteAccount, '/api/user/delete/')
    api.add_resource(SetUp, '/api/room/setup/')
    api.add_resource(Join, '/api/room/join/')
    api.add_resource(ChangeRoomPassword, '/api/room/change/')
    api.add_resource(Leave, '/api/room/leave/')
    api.add_resource(Status, '/api/room/status/')
    api.add_resource(GetRoom, '/api/room/roomdata/')
    api.add_resource(ChangeNotice, '/api/room/notice/')
    socketio.on_namespace(RoomData())
else:
    # 微信小程序
    from app.api.wechat.authentication import Login, ReName

    api.add_resource(Login, '/api/user/login/')
    api.add_resource(ReName, '/api/user/rename/')

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, host='0.0.0.0', port=80)
