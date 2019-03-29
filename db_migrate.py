# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app,db

manage = Manager(app)
migrate = Migrate(app,db)
manage.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manage.run()