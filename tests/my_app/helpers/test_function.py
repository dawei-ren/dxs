import unittest
from myApp.helpers.function import *


class TestFunc(unittest.TestCase):  # unittest.TestCase
    # 如果想在所有case执行之前准备一次测试环境，并在所有case执行结束后再清理环境
    @classmethod
    def setUpClass(cls):
        print("this setupclass() method only called once")

    @classmethod
    def tearDownClass(cls):
        print("this teardownclass() method only called once too")

    # 测试方法均已test开头，否则是不被unittest识别的
    def test_add(self):
        print("add:")
        self.assertEqual(3,add(1,2))

    def test_minus(self):
        print("minus")
        self.assertEqual(3,minus(5,2))

    # 如果想临时跳过某个case：skip装饰器
    @unittest.skip("i don't want to run this case. ")
    def test_multi(self):
        print("multi")
        self.assertEqual(6,multi(2,3))

    def test_divide(self):
        print("divide")
        self.assertEqual(2.5,divide(5,2))


if __name__ == "__main__":
    # 在main()中加verbosity参数，可以控制输出的错误报告的详细程度
    # verbosity=*：默认是1；设为0，则不输出每一个用例的执行结果；2-输出详细的执行结果
    # unittest.libs(verbosity=2)
    unittest.main()
