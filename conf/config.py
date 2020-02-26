"""
配置类.

主要用来调用配置文件
"""
import os
from configparser import ConfigParser

conf = ConfigParser()
conf.read('all.yaml')

#section = conf.sections()
#print(section)
#db = conf.options("db")
#db = conf.items("db")
#print(db)

# 获取绝对路径
BASE_DIR = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "all.yaml")  # 配置文件名称


class MyConfig:
    def __init__(self):
        self.__config = ConfigParser()
        self.__config.read(CONFIG_FILE_PATH)

    def conf(self):
        res = {}
        for i in self.__config.sections():
            section_dict = {}
            for j in self.__config.items(i):
                section_dict[j[0]] = j[1]
            res[i] = section_dict
        return res

    def develop(self):
        neo4j_dict = self.conf()["develop"]
        return neo4j_dict

    def test(self):
        neo4j_dict = self.conf()["test"]
        return neo4j_dict


myConfig = MyConfig()

myConf = myConfig.conf()

testConf = myConfig.test()
devConf = myConfig.develop()

if __name__ == "__main__":
    print(myConf)
    print(devConf)
