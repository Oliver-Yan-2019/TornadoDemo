from core.handlers.handler_base import BaseHandler
from libs.handler import open_handler


@open_handler(paths=r'/ping')
class PingHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.write('I\'m alive!')
