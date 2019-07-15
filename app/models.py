# encoding: utf-8
from app import db
from app.config import FlaskConfig
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40))
    openid = db.Column(db.String(128), nullable=False, index=True)
    unionid = db.Column(db.String(128), nullable=False)
    # email = db.Column(db.String(40), nullable=False)
    # password_hash = db.Column(db.String(128), nullable=False)
    birthday = db.Column(db.String(40))  # 前端说得弄string
    individuality = db.Column(db.String(128))
    gender = db.Column(db.SmallInteger)
    icon = db.Column(db.SmallInteger)
    # confirmed = db.Column(db.Boolean, default=False)
    registration_time = db.Column(db.DateTime, default=datetime.now)
    joined_room = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=60 * 60 * 24):
        serialize = Serializer(FlaskConfig.SECRET_KEY, expires_in=expiration)
        return serialize.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serialize = Serializer(FlaskConfig.SECRET_KEY)
        try:
            data = serialize.loads(token)
        except SignatureExpired:
            return None  # token已过期
        except BadSignature:
            return None  # token无效
        user = User.query.get(data['id'])
        return user

    def get_data(self):
        data = {}
        data['user_id'] = self.id
        data['username'] = self.username
        # data['email'] = self.email
        data['icon'] = self.icon
        data['individuality'] = self.individuality
        data['birthday'] = self.birthday
        data['gander'] = self.gender
        # data['confirmed'] = self.confirmed
        data['registration_time'] = self.registration_time
        data['joined_room'] = self.joined_room
        return data

    # def __del__(self):
    #     db.session.close()


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, nullable=False)
    room_name = db.Column(db.String(50), nullable=False)
    room_size = db.Column(db.SmallInteger, nullable=False)
    room_password = db.Column(db.String(128), nullable=False)
    count = db.Column(db.Integer, nullable=False, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    notice = db.Column(db.Text, default='')

    def get_data(self):
        data = {}
        data['room_id'] = self.id
        data['room_name'] = self.room_name
        data['owner_id'] = self.owner_id
        data['room_size'] = self.room_size
        data['count'] = self.count
        data['create_time'] = self.create_time
        return data

    def get_name(self):
        data = [rm.user[0].username for rm in self.roommembers]
        return data

    # def __del__(self):
    #     db.session.close()


class RoomMember(db.Model):
    __tablename__ = 'roommembers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    room = db.relationship('Room', backref='roommembers', foreign_keys=room_id)
    user = db.relationship('User', backref='roommember', foreign_keys=user_id)
    action = db.Column(db.String(8))

    def get_data(self):
        data = {}
        data['user_id'] = self.user_id
        data['join_time'] = self.join_time
        data['username'] = self.user.username
        return data

    # def __del__(self):
    #     db.session.close()
