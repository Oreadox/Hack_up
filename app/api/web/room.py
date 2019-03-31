# encoding: utf-8
from flask_restful import Resource, reqparse, abort, request
from flask import g, jsonify
from ...model.web_models import Room, User, RoomMember
from ...message import success_msg, fail_msg
from ... import db, auth


class SetUp(Resource):
    '建立房间'

    @auth.login_required
    def post(self):
        if g.user.joined_room:
            return fail_msg('你已经在一个房间了')
        request_data = request.get_json(force=True)
        room_name = request_data.get('room_name')
        room_size = request_data.get('room_size')
        room_password = request_data.get('room_password')
        if not room_name or not room_password:
            return fail_msg('房间名或房间密码不能为空')
        if not room_size:
            return fail_msg('请选择房间大小')
        room = Room(owner_id=g.user.id, room_name=str(room_name),
                    room_password=room_password, room_size=room_size)
        g.user.joined_room = True
        db.session.add(room)
        db.session.commit()
        db.session.add(RoomMember(room_id=room.id, user_id=g.user.id))
        db.session.commit()
        return success_msg(msg='房间建立成功', data={'room_id': room.id})


class Join(Resource):
    '加入房间'

    @auth.login_required
    def post(self):
        if g.user.joined_room:
            return fail_msg('你已经在一个房间了')
        request_data = request.get_json(force=True)
        room_id = request_data.get('room_id')
        room_password = request_data.get('room_password')
        if not room_id or not room_password:
            return fail_msg('房间号和密码不能为空！')
        room = Room.query.filter_by(id=room_id).first()
        if not room:
            return fail_msg('房间不存在！')
        if room.room_password != room_password:
            return fail_msg('密码错误！')
        if room.count >= room.size:
            return fail_msg('房间已满')
        room.count = room.count + 1
        g.user.joined_room = True
        db.session.add(RoomMember(room_id=room.id, user_id=g.user.id))
        db.session.commit()
        return success_msg(msg='房间加入成功', data={'room_id': room.id})


class ChangeRoomPassword(Resource):
    '更改房间密码'

    @auth.login_required
    def post(self):
        request_data = request.get_json(force=True)
        password = request_data.get('new_password')
        if not password:
            return fail_msg('密码不能为空！')
        if not g.user.joined_room:
            return fail_msg('未加入房间！')
        room = g.user.roommember.room
        if room.owner_id != g.user.id:
            return fail_msg('只有房主才能更改密码')
        room.room_password = password
        db.session.commit()
        return success_msg('密码更改成功！')


class Leave(Resource):
    '离开房间'

    # 房主离开为删除房间

    @auth.login_required
    def post(self):
        if not g.user.joined_room:
            return fail_msg('你未在任何一个房间')
        room = g.user.roommember.room
        if g.user.id == room.owner_id:
            for rm in room.roommembers:
                db.session.delele(rm)
            db.session.delete(room)
        else:
            db.session.delete(g.user.roommember)
            room.count = room.count - 1
        g.user.joined_room = False
        db.commit()
        return success_msg('房间离开成功！')


class Status(Resource):
    '用户及房间信息'

    @auth.login_required
    def get(self):
        data = {}
        user = g.user
        data['user'] = user.get_data()
        if user.joined_room:
            room = user.roommenber.room
            data['room'] = room.get_data()
        return success_msg(data=data)
