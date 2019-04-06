# encoding: utf-8
from flask_restful import Resource, reqparse, abort, request
from flask import g, jsonify
from app.models import Room, User, RoomMember
from app.message import success_msg, fail_msg
from app import db, auth


class RoomData(Resource):
    '房间相关'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('room_id', type=int)

    @auth.login_required
    def get(self):
        '获取指定房间信息'
        request_data = self.parser.parse_args()
        room_id = request_data.get('room_id')
        room = Room.query.filter_by(id=room_id).first()
        data = room.get_data()
        data['roommates'] = room.get_name()
        return success_msg(data=data)

    @auth.login_required
    def post(self):
        '新建房间'
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

    @auth.login_required
    def put(self):
        '修改房间信息'
        data = request.get_json(force=True)
        user = g.user
        if not user.joined_room:
            return fail_msg('未加入任何一个房间！')
        room = user.roommenber[0].room
        room.notice = data.get('notice') if data.get('notice') else room.notice
        is_owner = room.owner_id == user.id
        if is_owner:
            room.room_name = data.get('room_name') if data.get('room_name') else room.room_name
            room.room_password = data.get('room_password') if data.get('room_password') else room.room_password
            if data.get('room_size'):
                if int(room.room_size) <= int(data.get('room_size')):
                    room.room_size = data.get('room_size')
            return success_msg(msg='修改成功')
        elif (data.get('room_name') or data.get('room_password') or data.get('room_size')):
            return fail_msg('非创建者不能修改重要信息')

    def delete(self):
        '房间创建者删除房间'
        user = g.user
        if not user.joined_room:
            return fail_msg('你未在任何一个房间')
        room = g.user.roommember[0].room
        if user.id != room.owner_id:
            return fail_msg('非创建者无权删除房间')
        for rm in room.roommembers:
            rm.user.joined_room = False
            db.session.delele(rm)
        db.session.delete(room)
        user.joined_room = False
        db.session.coomit()
        return success_msg()


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
        if room.count >= room.room_size:
            return fail_msg('房间已满')
        room.count = room.count + 1
        g.user.joined_room = True
        db.session.add(RoomMember(room_id=room.id, user_id=g.user.id))
        db.session.commit()
        return success_msg(msg='房间加入成功', data={'room_id': room.id})

    @auth.login_required
    def delete(self):
        '离开房间'
        if not g.user.joined_room:
            return fail_msg('你未在任何一个房间')
        room = g.user.roommember[0].room
        db.session.delete(g.user.roommember[0])
        room.count = room.count - 1
        g.user.joined_room = False
        db.commit()
        return success_msg('房间离开成功！')
