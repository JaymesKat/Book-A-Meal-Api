from flask import Blueprint

default = Blueprint('default', __name__, template_folder='templates')

from . import views
