"""
user 接口单元测试
"""
import requests
import unittest
import json
import time


class TestUser(unittest.TestCase):
    """
    用户测试类
    """
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.user_url = self.base_url + "/myapp/api/v1/user"
        
    def test_post_user(self):

        headers = {'content-type': 'application/json'}

        random_name = 'name_' + str(time.time())

        password = 'passwd'

        data = {
            "name": random_name,
            "password": password
        }

        result = requests.post(url=self.user_url, data=json.dumps(data), headers=headers)
        result = result.json()
        self.assertEqual(result["success"], 1)


if __name__ == '__main__':
    unittest.main()