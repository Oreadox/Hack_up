# encoding: utf-8

import os


class FlaskConfig():
    DEBUG = True
    SECRET_KEY = "S83rQ53gC4vdarcIAvY89Ky4"
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'db1'
    USERNAME = 'user'
    PASSWORD = 'user'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 465 or 994
    # MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    BLOG_MAIL_SUBJECT_PREFIX = 'none'
    BLOG_MAIL_SENDER = MAIL_USERNAME
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False


class WechatProgramConfig():
    appid = os.environ.get('appid')
    secret = os.environ.get('appSecret')
    # access_token = os.environ.get('access_token')
