from . import db
from .config import AppConfig
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import desc
from itsdangerous import Serializer, BadSignature


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.DECIMAL(9,6), nullable=False)
    longitude = db.Column(db.DECIMAL(9,6), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

    def serialize(self):
        return {'latitude': str(self.latitude),
                'longitude': str(self.longitude),
                'timestamp': self.timestamp.isoformat()+'Z'  # HACK
                }


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    locations = db.relationship('Location', backref='device', lazy='select')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    db.UniqueConstraint('name', 'user_id')

    @property
    def last_location(self):
        return Location.query.filter_by(device_id=self.id).order_by(desc('location.id')).first()

    def get_device_dict(self):
        device_dict = {'id': self.id, 'name': self.name}
        if self.last_location:
            device_dict['last_location'] = self.last_location.serialize()
        return device_dict

    def generate_auth_token(self):
        s = Serializer(AppConfig.SECRET_KEY)
        return s.dumps(self.id)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(AppConfig.SECRET_KEY)
        try:
            id = s.loads(token)
        except BadSignature:
            return None
        device = Device.query.get(id)
        return device

    @staticmethod
    def get_by_devicename(user, name):
        device_list = user.devices
        for device in device_list:
            if device.name == name:
                return device
        return None


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password_hash = db.Column(db.Text)
    devices = db.relationship('Device', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def verify_credentials(username, password):
        user = User.get_by_username(username)
        if user is not None and user.check_password(password):
            return user
        return None

    def __repr__(self):
        return "<User '{}'>".format(self.username)
