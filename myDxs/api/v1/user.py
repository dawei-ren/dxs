from flask_restful import Resource
from flask import request
from myDxs.libs import utils
from myDxs.dbs import api
import datetime


class User(Resource):
    """
    用户
    """
    def get(self):
        """
        请求示例
        
        获取全部用户
        http://localhost:8000/dxs/api/v1/user
        """
        query = request.args

        filter_allowed_keys = ['name']
        filters = utils.get_filter(query, filter_allowed_keys)
        sort = utils.get_sort(query)
        limit = utils.get_limit(query)

        count, user_list = api.get_obj('user', filters=filters, sort=sort, limit=limit)

        for u in user_list:
            u.pop('password')

        if limit:
            return utils.common_resp(1, {
                "page": query.get('page'),
                "pageSize": query.get('pageSize'),
                "results": user_list,
                "totalCount": count
            })

        else:
            return utils.common_resp(1, {
                "results": user_list,
                "totalCount": count
            })

    def post(self):
        """
        {
          "name": "name1",
          "password": "passwd"
        }
        """
        json_data = request.json
        val, msg = utils.data_val(json_data, needed=['name', 'password'])

        if val:
            name = json_data['name']
            if not name:
                return utils.common_resp(0, "用户名不能为空")
            cnt, judge_name = api.get_obj('user', [f'name="{name}"'])

            if cnt:
                return utils.common_resp(0, f'{name}已经存在')

            else:
                password = json_data['password']
                json_data.update(
                    {'created_time': datetime.datetime.now(),
                     'updated_time': datetime.datetime.now(),
                     'name': name,
                     'password': password
                     }
                )

                ret = api.save_obj('user', json_data)
                ret.pop('password')
                return utils.common_resp(1, ret)

        else:
            return utils.common_resp(0, msg)
