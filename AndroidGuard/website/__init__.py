from flask import Blueprint

main = Blueprint('website', __name__)

from . import views
