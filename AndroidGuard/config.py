import os

basedir = os.path.abspath(os.path.dirname(__file__))


# application configuration object
class AppConfig:
    # TODO: generate your secret key
    SECRET_KEY = ''
    # TODO: add your google maps javascript API key
    GOOGLEMAPS_KEY = ''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'androidguard.db')
    # TODO: add your firebase cloud messaging API key
    FCM_API_KEY = ''
    FCM_PROXY_DICT = {
        "http": "http://127.0.0.1",
        "https": "http://127.0.0.1",
    }
