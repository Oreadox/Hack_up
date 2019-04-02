# encoding: utf-8

from flask_socketio import emit, Namespace, send, join_room
from datetime import datetime
from ...model.web_models import User


class RoomData(Namespace):

    def on_get_time(self, msg):
        '''测试用'''
        print('ok')
        time = str(datetime.now())
        emit('time', {'time': time})

    def on_connect(self):
        send('连接成功')

    def on_join_room(self, data):
        token = ''
        if data.get('token'):
            token = data.get('token')[7:]
        else:
            emit('join_room', {'message': '需要token'})
        user = User.verify_auth_token(token)
        if not user:
            emit('join_room', {'message': 'token失效'})
        if not user.joined_room:
            emit('join_room', {'message': '未加入房间'})
        room = user.roommember.room
        join_room(room='room_' + str(room.id))
        join_room(room=user.id)
        msg = []
        for rm in room.roommembers:
            dict = {}
            dict['user_id'] = rm.user.id
            ##还没写完
            msg.append(dict)
        emit('last_data', msg)

    def on_message(self, data):
        user_id = data.get('user_id')
        message = data.get('message')
        time = str(datetime.now())
        user = User.query.filter_by(id=user_id).first()
        msg = {
            'user_id': user_id,
            'message': message,
            'time': time
        }
        room = user.roommember.room
        emit('message', msg, room='room_' + str(room.id))
