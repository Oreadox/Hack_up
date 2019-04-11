# encoding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api
from flask_cors import CORS
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_socketio import SocketIO
from .config import FlaskConfig

app = Flask(__name__)
app.config.from_object(FlaskConfig)
db = SQLAlchemy(app)
auth = HTTPTokenAuth()
CORS(app, supports_credentials=True)
api = Api(app)
mail = Mail(app)
CSRFProtect(app)
socketio = SocketIO(app)

from app.models import User
from flask import g


@app.before_request
def before_request():
    g.error = ''


@app.after_request
def after_request(resp):
    db.session.close()
    return resp


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True
