# encoding: utf-8

from flask_restful import Resource, reqparse, abort, request
from flask import g, jsonify
from app.models import User, Room
from app import db, auth
from app.message import fail_msg, success_msg
from .form.user import SignupForm, LoginForm, ChangePasswordForm, ForgetPasswordForm
from app.email import send_email


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
        '新建用户'
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

    @auth.login_required
    def put(self):
        '修改用户信息(除密码)'
        user = g.user
        data = request.get_json(force=True)
        # if data.get('username'):
        #     username = data.get('username')
        #     if User.query.filter(User.username == username, User.id != g.user.id).all():
        #         return fail_msg(msg='该用户名已存在！')
        #     user.username = username
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


class Token(Resource):
    'token相关'

    def post(self):
        '新建(获取)token(登录)'
        form = LoginForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = User.query.filter_by(username=form.username.data).first() or \
               User.query.filter_by(email=form.username.data).first()
        if not user:
            return fail_msg("该用户不存在！")
        if not user.verify_password(password=form.password.data):
            return fail_msg("密码错误！")
        token = user.generate_auth_token()
        return ({'token': token.decode('ascii')})


class Password(Resource):
    '用户密码'

    @auth.login_required
    def put(self):
        '修改密码(需原密码)'
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

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)

    def post(self):
        '修改密码（需要邮箱已验证）[此处仅验证邮箱及发送邮件]'
        form = ForgetPasswordForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = User.query.filter_by(username=form.username.data, email=form.email.data).first()
        if not user:
            return fail_msg('该用户不存在！')
        # send_email()  # 此处以后再修改
        return success_msg(msg="邮件已发送")

    def get(self):
        '获取网页'
        from flask import render_template
        return render_template("")

    def put(self):
        '修改密码'
        pass


class Email(Resource):
    '用户邮箱'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)

    def get(self):
        '修改邮箱验证状态'
        data = self.parser.parse_args()
        user = User.verify_auth_token(data.get('id'))
        if not user:
            abort(404)
            return None
        user.confirmed = True
        db.session.commit()
        return success_msg()
