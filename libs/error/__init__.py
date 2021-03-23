from tornado.web import HTTPError


class AppError(HTTPError):

    def __init__(self, status_code: int = 500, log_code: int = 100000, log_content: str = ''):
        self.log_message = f'{log_code}:{log_content}'
        super(AppError, self).__init__(status_code, self.log_message)

    def description(self, description: str):
        self.log_message = f'{self.log_message}:{description}'


ARGUMENT_ILLEGAL = AppError(500, 100000, '参数非法')
