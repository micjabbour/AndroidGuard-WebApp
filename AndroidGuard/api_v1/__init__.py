from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

api_v1 = Blueprint('api_v1', __name__)
auth = HTTPBasicAuth()

from . import views
