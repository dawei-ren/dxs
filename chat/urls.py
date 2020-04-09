from flask_restful import Api
from chat.api.v1 import user, health

from . import chat_app

api = Api(chat_app)

api.add_resource(user.User, '/api/v1/user')
api.add_resource(health.Health, '/api/v1/health')
