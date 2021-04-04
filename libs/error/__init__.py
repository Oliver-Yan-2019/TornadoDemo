from tornado.web import HTTPError


class AppError(HTTPError):

    def __init__(self, status_code: int = 500, log_code: int = 100000, log_content: str = ''):
        self.log_message = f'{log_code}:{log_content}'
        super(AppError, self).__init__(status_code, self.log_message)

    def description(self, description: str):
        self.log_message = f'{self.log_message}:{description}'


ARGUMENT_ILLEGAL = AppError(500, 100000, '参数非法')
KEY_NOT_FOUND = AppError(500, 100001, '没有找到关键值')

PASSWORD_ILLEGAL = AppError(500, 110000, '密钥非法')

SUBCLASS_ILLEGAL = AppError(500, 120000, '非法子类')
