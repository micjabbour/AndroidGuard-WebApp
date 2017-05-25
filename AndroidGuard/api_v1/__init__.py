from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

api_v1 = Blueprint('api_v1', __name__)
creds_auth = HTTPBasicAuth()  # authentication using username/password
token_auth = HTTPBasicAuth()  # authentication using device token

from . import views
