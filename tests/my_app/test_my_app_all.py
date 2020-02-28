from tests.my_app.helpers.test_class import TestClass
from tests.my_app.helpers.test_function import TestFunc
from tests.my_app.api.v1.test_user import TestUser
import unittest
from flask import Flask

app = Flask(__name__)


def test_class_suit():
    suite_class = unittest.TestLoader(). \
        loadTestsFromTestCase(TestClass)
    return suite_class


def test_func_suit():
    suite_func = unittest.TestLoader(). \
        loadTestsFromTestCase(TestFunc)
    return suite_func


def test_user_suit():
    suite_user = unittest.TestLoader(). \
        loadTestsFromTestCase(TestUser)
    return suite_user


def test_my_app_all():
    test_all = [
        test_class_suit(),
        test_func_suit(),
        test_user_suit()
    ]

    suite = unittest.TestSuite(test_all)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_my_app_all())


