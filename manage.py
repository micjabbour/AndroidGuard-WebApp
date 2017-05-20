from flask_script.cli import prompt_bool

from AndroidGuard import app, db
from flask_script import Manager
from AndroidGuard.models import User

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    print('Initialized the database.')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop the database"):
        db.drop_all()
        print('Dropped the database.')

if __name__ == '__main__':
    manager.run()