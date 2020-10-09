class AppError(Exception):
    """
    统一应用错误对象，返回错误编码和消息
    """
    def __init__(self, msg="you've got a error!", code=400):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg


class DBError(AppError):
    def __init__(self, msg='数据库操作异常', code=500):
        super(DBError, self).__init__(msg, code)


class ParaValidateFailError(AppError):
    def __init__(self, msg='数据库操作异常', code=400):
        super(ParaValidateFailError, self).__init__(msg, code)
