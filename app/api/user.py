# encoding: utf-8

from flask_restful import Resource, reqparse, abort, request
from flask import g, jsonify
import requests
from app.models import User, Room
from app import db, auth
from app.message import fail_msg, success_msg
from ..config import WeChatConfig


class UserData(Resource):
    '用户(当前登录用户)'

    @auth.login_required
    def get(self):
        '获取当前用户及房间信息'
        data = {}
        user = g.user
        data['user'] = user.get_data()
        data['room'] = {}
        data['roommates'] = []
        if user.joined_room:
            room = user.roommember[0].room
            data['room'] = room.get_data()
            for rm in room.roommembers:
                data['roommates'].append(rm.get_data())
        return jsonify(success_msg(data=data))

    def post(self):
        '新建用户&登录'
        request_data = request.get_json(force=True)
        code = request_data.get('code')
        if not code:
            return jsonify(fail_msg(msg='code为空'))
        payload = {
            'appid': WeChatConfig.appid,
            'secret': WeChatConfig.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=payload)
        resp = r.json()
        if resp.errcode:
            return fail_msg(msg=resp.errmsg)
        if User.query.filter_by(openid=resp.openid).first():
            token = self.token(user=User.query.filter_by(openid=resp.openid).first())
            return jsonify(token)
        user = User(openid=resp.openid, unionid=resp.unionid)
        db.session.add(user)
        db.session.commit()
        token = self.token(user=user)
        return jsonify(token)

    @auth.login_required
    def put(self):
        '修改用户信息'
        user = g.user
        data = request.get_json(force=True)
        user.username = data.get('username') if data.get('username') else user.username
        user.birthday = data.get('birthday') if data.get('birthday') else user.birthday
        user.individuality = data.get('individuality') if data.get('individuality') else user.individuality
        user.gender = data.get('gender') if data.get('gender') else user.gender
        user.icon = data.get('icon') if data.get('icon') else user.icon
        db.session.commit()
        return success_msg()

    @auth.login_required
    def delete(self):
        '删除用户'
        db.session.delete(g.user)
        db.session.commit()
        return success_msg

    @staticmethod
    def token(user):
        '新建token'
        token = user.generate_auth_token()
        return ({'token': token.decode('ascii')})

