# encoding: utf-8
from .. import db
from ..config import FlaskConfig
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), index=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    room_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

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


class Room(db.Model):
    __tablename__ = 'rooms'
