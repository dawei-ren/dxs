from flask_restful import Resource
from flask import request
from myDxs.libs import utils
from myDxs.libs import token
from myDxs.dbs import api, models
import datetime
from werkzeug.security import check_password_hash


class Login(Resource):
    """
    用户
    """
    def post(self):
        """
        请求示例
        
        用户登录
        http://localhost:8000/dxs/api/v1/login
        """
        json_data = request.json
        name = json_data['name']
        password = json_data['password']

        if not name:
            return utils.common_resp(0, "用户名不能为空")
        if not password:
            return utils.common_resp(0, "密码不能为空")
        cnt, user = api.get_obj_obj('user', [f'name="{name}"'])

        user_data = user[0]
        if not cnt:
          return utils.common_resp(0, "用户名不存在")
        if not user_data.check_password(password):
          return utils.common_resp(0, "密码错误")
        user_token =  token.create_token(user_data.id)
        res = {
            "token": user_token,
            "username": user_data.name
          }
        return utils.common_resp(1, res)
