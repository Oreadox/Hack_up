# encoding: utf-8
from .. import db
from ..config import FlaskConfig
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature


class WechatUser(db.Model):
    __tablename__ = 'wechat_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(32), index=True, nullable=False)
    # author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(40), index=True)

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
        user = WechatUser.query.get(data['id'])
        return user
