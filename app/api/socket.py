# encoding: utf-8

from flask_socketio import emit, Namespace, send, join_room, leave_room
from datetime import datetime
from app.models import User


class RoomData(Namespace):

    def verify_token(token):
        user = User.verify_auth_token(token)
        err = ''
        if not user:
            message = {'message': 'token失效'}
        return user, err

    def on_get_time(self, msg):
        '''测试用'''
        print('ok')
        time = str(datetime.now())
        emit('time', {'time': time})

    def on_join_room(self, data):
        token = data.get('token')
        if not token:
            emit('join_room', {'message': '需要token'})
            return None
        user, err = self.verify_token(token)
        if err:
            emit('join_room', err)
            return None
        if not user.joined_room:
            emit('join_room', {'message': '未加入房间'})
            return None
        room = user.roommember[0].room
        join_room(room='room_' + str(room.id))
        join_room(room=user.id)
        emit('join_room', {'user_id': user.id})
        msg = []
        for rm in room.roommembers:
            dict = {}
            dict['user_id'] = rm.user.id
            ##还没写完
            msg.append(dict)
        emit('last_data', msg)

    def on_leave_room(self, data):
        token = data.get('token')
        if not token:
            emit('join_room', {'message': '需要token'})
            return None
        # user_id = data.get('user_id')
        user, err = self.verify_token(token)
        if err:
            emit('leave_room', err)
            return None
        # if not user_id:
        #     emit('leave_room', {'message': '需要用户id'})
        #     return None
        # user = User.query.filter_by(id=user_id).first()
        # if not user:
        #     emit('leave_room', {'message': '该用户不存在'})
        #     return None
        room = user.roommember[0].room
        leave_room(room='room_' + str(room.id))
        leave_room(room=user.id)

    def on_message(self, data):
        token = data.get('token')
        if not token:
            emit('join_room', {'message': '需要token'})
            return None
        user, err = self.verify_token(token)
        if err:
            emit('on_message', err)
            return None
        # user_id = data.get('user_id')
        message = data.get('message')
        time = str(datetime.now())
        # user = User.query.filter_by(id=user_id).first()
        # if not user:
        #     emit('leave_room', {'message': '该用户不存在'})
        #     return None
        msg = {
            'user_id': user.id,
            'message': message,
            'time': time
        }
        room = user.roommember[0].room
        emit('message', msg, room='room_' + str(room.id))
