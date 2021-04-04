from markdown import markdown
from os.path import join

from core.handlers.handler_base import BaseHandler
from libs.handler import open_handler
from environment import BASE_DIR
from utils import Obj


@open_handler(paths=['/', '/home'])
class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        record_list = [
            {
                'title': '日志1',
                'img_url': 'http://127.0.0.1:8000/static/img/background.jpeg?v=a641fd53477491d9246aa164504faad4',
                'img_desc': '背景图1',
                'content': '测试内容1',
                'datetime': '2021年4月1日'
            },
            {
                'title': '日志2',
                'img_url': 'http://127.0.0.1:8000/static/img/background.jpeg?v=a641fd53477491d9246aa164504faad4',
                'img_desc': '背景图2',
                'content': '测试内容2',
                'datetime': '2021年4月1日'
            }
        ]
        self.render('home/home.html', record_list=[Obj(r) for r in record_list])


@open_handler(paths=['/article'])
class ArticleHandler(BaseHandler):
    def get(self, *args, **kwargs):
        with open(join(BASE_DIR, 'statics/article/markdown/README.md')) as f:
            html = markdown(f.read())
            self.render('article/article.html', markdown=html, nav_list=[])
