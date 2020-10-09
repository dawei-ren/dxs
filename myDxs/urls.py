from flask_restful import Api
from myDxs.api.v1 import user, health

from . import my_dxs

api = Api(my_dxs)

api.add_resource(user.User, '/api/v1/user')
api.add_resource(health.Health, '/api/v1/health')
