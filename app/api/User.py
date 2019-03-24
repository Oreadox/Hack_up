# encoding: utf-8

from flask_restful import Resource, reqparse, request
from flask import g, make_response
from ..models import User
from .. import db,auth
from ..message import fail_msg,success_msg
from .form.User import SignupForm,LoginForm


class Login(Resource):
    '登录'

    def post(self):
        form = LoginForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = User.query.filter_by(username=form.username_or_email.data).first() or \
               User.query.filter_by(email=form.username_or_email.data).first()
        if not user.verify_password(password=form.password.data):
            return fail_msg("密码错误！")
        token = user.generate_auth_token()
        return ({'token': token.decode('ascii')})


class SingUp(Resource):
    '注册'

    def post(self):
        form = SignupForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = User(username=form.username.data,email=form.email.data)
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return success_msg()


class Logout(Resource):
    '登出'

    def get(self):
        pass

class ChangePassword(Resource):
    '修改密码'

    def put(self):
        form = SignupForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = User.query.filter_by(username=form.username.data,password=form.password.data).first()
        if not user:
            return fail_msg("密码错误！")
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return success_msg()


@auth.login_required
class DeleteAccount(Resource):
    '删除账户'

    def delete(self):
        db.session.delete(g.user)
        db.session.commit()
        return success_msg
