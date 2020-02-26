from flask_restful import Api
from myApp.api.v1 import user, health

from . import my_app

api = Api(my_app)

api.add_resource(user.User, '/api/v1/user')
api.add_resource(health.Health, '/api/v1/health')
