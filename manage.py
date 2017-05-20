from flask_script.cli import prompt_bool

from AndroidGuard import app, db
from flask_script import Manager
from AndroidGuard.models import User, Device, Location

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    u= User(username='user1', password='123')
    d1= Device(name='device1', user=u)
    l1= Location(latitude=1.1, longitude=1.1, device=d1)
    l2= Location(latitude=2.2, longitude=2.2, device=d1)
    l3 = Location(latitude=3.3, longitude=3.3, device=d1)
    d2 = Device(name='device2', user=u)
    l= Location(latitude=4.4, longitude=4.4, device=d2)
    db.session.add(u)
    db.session.add(d1)
    db.session.add(l1)
    db.session.add(l2)
    db.session.add(l3)
    db.session.add(d2)
    db.session.add(l)
    db.session.commit()
    print('Initialized the database.')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop the database"):
        db.drop_all()
        print('Dropped the database.')

if __name__ == '__main__':
    manager.run()
