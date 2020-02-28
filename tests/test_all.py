from tests.my_app.helpers import test_class, test_function
from tests.my_app.api.v1 import test_user
from tests.my_app import test_my_app_all
import unittest
from flask import Flask

app = Flask(__name__)


@app.cli.command('test_all', help='单元测试')
def test_all():

    suite = unittest.TestSuite()

    my_app = test_my_app_all.test_my_app_all()

    all_test = [
        my_app,
    ]
    suite.addTests(all_test)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':

    suite = unittest.TestSuite()
    # 定义list，按照list里的顺序执行测试用例
    tests = [
        test_function.TestFunc("test_add"),
        test_function.TestFunc("test_minus"),
        test_function.TestFunc("test_multi"),
        test_function.TestFunc("test_divide"),
        test_class.TestClass("test_class_sum"),
        test_class.TestClass("test_class_sub"),
        test_user.TestUser("test_post_user")
    ]
    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

