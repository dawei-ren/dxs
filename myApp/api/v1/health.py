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
        /myapp/v1/test

        :return:
        """

        return utils.common_resp(1, {
            "results": "Hello World",
        })


