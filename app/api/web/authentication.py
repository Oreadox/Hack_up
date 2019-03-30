# encoding: utf-8

from flask_restful import Resource, reqparse, abort
from flask import g
from ...model.web_models import User
from ... import db, auth
from ...message import fail_msg, success_msg
from .form.authentication import SignupForm, LoginForm, ChangePasswordForm
from ...email import send_email


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
        if not user:
            return fail_msg("该用户不存在！")
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
        user = User(username=form.username.data, email=form.email.data)
        user.hash_password(form.password.data)
        # send_email()  # 此处以后再修改
        db.session.add(user)
        db.session.commit()
        return success_msg()


class Logout(Resource):
    '登出'

    def get(self):
        pass


class ChangePassword(Resource):
    '修改密码（需要原密码且已登录）'

    @auth.login_required
    def put(self):
        form = ChangePasswordForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = g.user
        user.hash_password(form.password.data)
        db.session.commit()
        return success_msg()


class ForgetPassword(Resource):
    '修改密码（需要邮箱已验证）[此处仅验证邮箱及发送邮件]'

    def post(self):
        form = ChangePasswordForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        # send_email()  # 此处以后再修改
        return success_msg(msg="邮件已发送")


class ResetPassword(Resource):
    '重置密码（从邮件中）'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)

    def get(self):
        from flask import render_template
        return render_template("")

    def put(self):
        pass


class UserConfirm(Resource):
    '验证邮箱'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)

    def get(self):
        data = self.parser.parse_args()
        user = User.verify_auth_token(data.get('id'))
        if not user:
            abort(404)
            return None
        user.confirmed = True
        db.session.commit()
        return success_msg()



class DeleteAccount(Resource):
    '删除账户'

    @auth.login_required
    def delete(self):
        db.session.delete(g.user)
        db.session.commit()
        return success_msg
