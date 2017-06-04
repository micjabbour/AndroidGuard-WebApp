from flask import Flask
from flask_pyfcm import FCM
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from .config import AppConfig

# db object
db = SQLAlchemy()
gm = GoogleMaps()
fcm = FCM()

# configure login manager
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "website.login"

# for displaying timestamps
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    gm.init_app(app)
    fcm.init_app(app)

    from .website import website as website_blueprint
    app.register_blueprint(website_blueprint, url_prefix='')

    from .api_v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app

app = create_app()

from . import models
