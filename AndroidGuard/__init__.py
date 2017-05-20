from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from .config import AppConfig

# db object
db = SQLAlchemy()
gm = GoogleMaps()

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

    from .website import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='')

    return app

app = create_app()

from . import models
