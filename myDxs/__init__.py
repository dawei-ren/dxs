from flask import Blueprint

my_dxs = Blueprint('myDxs', __name__)
from . import urls
