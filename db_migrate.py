# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app,db
from app.model.web_models import User
from app.model.wechat_app_models import WechatUser
from app.config import use_mysql

manage = Manager(app)
migrate = Migrate(app,db)
manage.add_command('db',MigrateCommand)


if __name__ == '__main__':
    if use_mysql:
        manage.run()
    else:
        db.drop_all()
        db.create_all()
