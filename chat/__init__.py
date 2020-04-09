from flask import Blueprint

chat_app = Blueprint('chat', __name__)
from . import urls
