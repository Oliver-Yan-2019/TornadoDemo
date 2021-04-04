from sys import argv

from tornado.ioloop import IOLoop
from tornado.web import (
    Application
)

from environment import environment


class App(Application):
    def __init__(self):
        """主程序"""

        environment.initialize()

        common_handlers, host_handlers = environment.get_handlers()
        settings = environment.get_tornado_settings()

        super(App, self).__init__(handlers=common_handlers, **settings)


def start_app():
    """主程序启动

    Returns:

    """

    app = App()
    app.listen(8000)  # HTTPServer
    IOLoop.current().start()  # 类的异步网络库, IOLoop和IOStream


if __name__ == '__main__':
    if len(argv) < 2:
        start_app()
    else:
        if argv[1] == 'update_table_structure':
            from core.base.model import Base

            environment.initialize()
            Base.metadata.create_all(environment.db_engine)
