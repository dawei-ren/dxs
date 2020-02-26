from flask import Blueprint

my_app = Blueprint('myApp', __name__)
from . import urls
