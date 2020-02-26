from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash


"""
数据库
"""

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    created_time = Column(DateTime, default=datetime.now())  # 创建时间
    updated_time = Column(DateTime, onupdate=datetime.now(), default=datetime.now())  # 更新时间


class DeletedModel(BaseModel):
    __abstract__ = True
    deleted = Column(String(length=1), default='0')  # 是否删除
    deleted_time = Column(DateTime, default='9999-01-01')  # 删除时间


class ModelDictMixin(object):

    @classmethod
    def from_dict(cls, d):
        """Return a model instance from a dictionary."""
        return cls(**d)

    def to_dict(self):
        """Return the model's attributes as a dictionary."""
        names = (column.name for column in self.__table__.columns)
        return {name: getattr(self, name) for name in names}

    @classmethod
    def column_names(cls):
        names = (column.name for column in cls.__table__.columns)
        return list(names)


class User(DeletedModel, ModelDictMixin):
    """用户表"""
    __tablename__ = 'myapp_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=255))  # 姓名
    password = Column(String(length=255), nullable=False)  # 登陆密码

    def set_password(self, password):
        """
        密码加密
        """
        self.password = generate_password_hash(password)
        return self.password

    def check_password(self, password):
        """
        验证密码，如果返回为True，则进行下一步操作
        """
        return check_password_hash(self.passwd, password)


MODELS = {
    'user': User,
}


if __name__ == '__main__':
    """
    初始化数据库，创建表
    """
    # print(Base.metadata.drop_all(bind=get_engine()))
    from myApp.dbs import engine
    print(Base.metadata.create_all(bind=engine))
    pass
