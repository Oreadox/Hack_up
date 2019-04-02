# encoding: utf-8

from flask_socketio import emit, Namespace, send, join_room, leave_room
from datetime import datetime
from ...model.web_models import User


class RoomData(Namespace):

    def on_get_time(self, msg):
        '''测试用'''
        print('ok')
        time = str(datetime.now())
        emit('time', {'time': time})

    def on_join_room(self, data):
        token = ''
        if data.get('token'):
            token = data.get('token')[7:]
        else:
            emit('join_room', {'message': '需要token'})
            return None
        user = User.verify_auth_token(token)
        if not user:
            emit('join_room', {'message': 'token失效'})
            return None
        if not user.joined_room:
            emit('join_room', {'message': '未加入房间'})
            return None
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

    def on_leave_room(self, data):
        user_id = data.get('user_id')
        if not user_id:
            emit('leave_room', {'message': '需要用户id'})
            return None
        user = User.query.filter_by(id=user_id).first()
        if not user:
            emit('leave_room', {'message': '该用户不存在'})
            return None
        room = user.roommember.room
        leave_room(room='room_' + str(room.id))
        leave_room(room=user.id)

    def on_message(self, data):
        user_id = data.get('user_id')
        message = data.get('message')
        time = str(datetime.now())
        user = User.query.filter_by(id=user_id).first()
        if not user:
            emit('leave_room', {'message': '该用户不存在'})
            return None
        msg = {
            'user_id': user_id,
            'message': message,
            'time': time
        }
        room = user.roommember.room
        emit('message', msg, room='room_' + str(room.id))
