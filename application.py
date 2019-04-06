# encoding: utf-8

from app import api, app, socketio

from app.api.user import UserData, Email, ForgetPassword, Token, Password
from app.api.room import RoomData, Join
from app.api.socket import RoomData as socket

api.add_resource(UserData, '/api/user/current')
api.add_resource(Email, '/api/user/email')
api.add_resource(ForgetPassword, '/api/user/forget')
api.add_resource(Token, '/api/user/token')
api.add_resource(Password, '/api/user/password')
api.add_resource(RoomData, '/api/room/data')
api.add_resource(Join, '/api/room/join')
socketio.on_namespace(socket())

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, host='0.0.0.0', port=80)
