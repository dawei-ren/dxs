from flask_restful import Resource
from flask import request
from myApp.libs import utils
from myApp.dbs import api
import datetime


class Health(Resource):
    """
    用户
    """
    def get(self):
        """
        请求示例
        http://localhost:8000/dxs/api/v1/health

        :return:
        """

        return utils.common_resp(1, {
            "results": "Hello World",
        })


