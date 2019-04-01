# encoding: utf-8

from app import socketio
from flask_socketio import emit, Namespace, send, join_room
from datetime import datetime
from ...model.web_models import User


class RoomData(Namespace):

    def on_get_time(self, msg):
        '''测试用'''
        print('ok')
        time = str(datetime.now())
        emit('time', {'time': time})

    def on_join_room(self, msg):
        if msg.get('token'):
            token = msg.get('token')[7:]
        else:
            emit('join_room', {'message': '需要token'})
        user = User.verify_auth_token(token)
        if not user:
            emit('join_room', {'message': 'token失效'})
        if not user.joined_room:
            emit('join_room', {'message': '未加入房间'})
        room = user.roommember.room
        join_room(room='room_' + str(room.id))
