# encoding: utf-8
from flask_restful import Resource, request
import requests, json
from flask import g
from ... import db, auth
from ...model.wechat_app_models import WechatUser as User
from ...message import fail_msg, success_msg
from ...config import WechatProgramConfig as Config


class Login(Resource):
    '登录'

    def post(self):
        request_data = request.get_json(force=True)
        login_code = request_data.get('login_code')
        if not login_code:
            return fail_msg(msg='用户临时登录code不能为空！')
        payload = {'appid': Config.appid, 'secret': Config.secret,
                   'js_code': login_code, 'grant_type': 'authorization_code'}
        r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=payload)
        data = json.loads(r.content.decode())
        if data.get('errcode'):
            return fail_msg(msg='系统繁忙！')
        openid = data.get('openid')
        user = User.query.filter_by(openid=openid).first()
        if not user:
            user = User(openid=openid)
            token = user.generate_auth_token()
            db.session.add(user)
            db.commit()
            return ({'token': token.decode('ascii'), 'named': False})
        token = user.generate_auth_token()
        return ({'token': token.decode('ascii'), 'named': user.username is not None})


class ReName(Resource):
    '用户重命名'

    @auth.login_required
    def post(self):
        request_data = request.get_json(force=True)
        if not request_data.get('name'):
            return fail_msg('无效输入!')
        user = g.user
        user.username = request_data.get('name')
        db.commit()
        return success_msg()