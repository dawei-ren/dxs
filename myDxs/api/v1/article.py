from flask_restful import Resource
from flask import request
from myDxs.libs import utils, token
from myDxs.dbs import api
import datetime


class Article(Resource):
    """
    用户
    """
    def get(self):
        """
        请求示例

        请求全部文章
        http://localhost:8000/dxs/api/v1/article

        按id搜索
        http://localhost:8000/dxs/api/v1/article?id=1

        按标题搜索
        http://localhost:8000/dxs/api/v1/article?title=归园田居

        按作者搜索
        http://localhost:8000/dxs/api/v1/article?author=王维

        分页
        http://localhost:8000/dxs/api/v1/article?page=1&pageSize=1

        排序
        http://localhost:8000/dxs/api/v1/article?sortby=title&order=desc

        :return:
        """
        
        query = request.args

        filter_allowed_keys = ['author', 'title','id']
        filters = utils.get_filter(query, filter_allowed_keys)
        sort = utils.get_sort(query)
        limit = utils.get_limit(query)

        count, article_list = api.get_obj('article', filters=filters, sort=sort, limit=limit)

        if limit:
            return utils.common_resp(1, {
                "page": query.get('page'),
                "pageSize": query.get('pageSize'),
                "results": article_list,
                "totalCount": count
            })

        else:
            return utils.common_resp(1, {
                "results": article_list,
                "totalCount": count
            })
            
    @token.login_required
    def post(self):
        """
        {
          "title": "归园田居",
          "author": "陶渊明",
          "content": "种豆南山下，草盛豆苗稀。 晨兴理荒秽，带月荷锄归。 道狭草木长，夕露沾我衣。 衣沾不足惜，但使愿无违",
        }
        """
        json_data = request.json
        val, msg = utils.data_val(json_data, needed=['title', 'author'])

        if val:
            title = json_data['title']
            if not title:
                return utils.common_resp(0, "标题不能为空")
            cnt, judge_title = api.get_obj('article', [f'title="{title}"'])

            if cnt:
                return utils.common_resp(0, f'{title}已经存在')

            else:
                content = json_data['content']
                author = json_data['author']
                json_data.update(
                    {'created_time': datetime.datetime.now(),
                     'updated_time': datetime.datetime.now(),
                     'title': title,
                     'content': content,
                     'author': author
                     }
                )

                ret = api.save_obj('article', json_data)
                
                return utils.common_resp(1, ret)

        else:
            return utils.common_resp(0, msg)

    # def delete(self):
    #     #
    #     return utils.common_resp(0, "aaa")
