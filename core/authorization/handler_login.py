from core.handlers.handler_base import BaseHandler

from libs.handler import open_handler

import heapq


@open_handler(paths='/login')
class LoginHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        await self.render("authorization/login.html")

    async def post(self, *args, **kwargs):
        self.redirect('https://something.lowercoder.com')
