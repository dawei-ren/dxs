import unittest
from myApp.helpers import help_class


# 单元测试模块
class TestClass(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        self.tclass = help_class.MyClass()

    # 退出清理工作
    def tearDown(self):
        pass

    def test_class_sum(self):
        self.assertEqual(self.tclass.sum(1, 2), 3)

    def test_class_sub(self):
        self.assertEqual(self.tclass.sub(2, 1), 1)


if __name__ == '__main__':
    unittest.main()