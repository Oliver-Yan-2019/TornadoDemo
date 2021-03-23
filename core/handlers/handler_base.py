from typing import Optional, Awaitable
from tornado.web import (
    RequestHandler,  # 创建Web应用程序和各种支持类的子类
)


class BaseHandler(RequestHandler):

    def initialize(self):
        pass

    def prepare(self):
        pass

    def on_finish(self):
        pass

    def set_default_headers(self):
        pass

    def get_current_user(self):
        pass

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def get(self, *args, **kwargs):
        pass

    async def post(self, *args, **kwargs):
        pass
