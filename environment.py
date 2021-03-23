from os.path import join, dirname
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from libs.handler.factory import HandlerFactory
from libs.singleton import singleton
from libs.config import Config
from libs.module_iter import module_iter

BASE_DIR = dirname(__file__)


@singleton
class Environment(object):
    def __init__(self):
        self.is_inited = False
        self.conf = Config()
        self.db_engine = None
        self.db_session = None

    def initialize(self):
        if self.is_inited is True:
            return

        self.init_config()
        self.init_database()
        self.module_iter_all()

    def init_config(self):
        for file_name in ['default', 'product', 'develop']:
            self.conf.initialize(join(BASE_DIR, 'config', f'{file_name}.conf'))

    def init_database(self):
        self.db_engine = create_engine(
            self.conf.get_conf('db', 'url'),
            convert_unicode=True,
            echo=self.conf.get_conf('db', 'echo', conf_type=bool),
            poolclass=QueuePool,
            pool_size=200,
            pool_recycle=100,
            max_identifier_length=128
        )
        self.db_session = scoped_session(sessionmaker(bind=self.db_engine))

    @staticmethod
    def get_handlers():
        handler_factory = HandlerFactory(module_libs=['core', 'apps'])
        return handler_factory.get_handlers()

    def get_tornado_settings(self):
        return dict(
            static_path=join(BASE_DIR, "statics"),
            # static_url_prefix="/server/static/",
            template_path=join(BASE_DIR, "templates"),
            cookie_secret=self.conf.get_conf('tornado', 'cookie_secret'),
            gzip=self.conf.get_conf('tornado', 'gzip', conf_type=bool),
            autoescape=self.conf.get_conf('tornado', 'auto_escape', conf_type=bool),
            debug=self.conf.get_conf('tornado', 'debug', conf_type=bool)
        )

    @staticmethod
    def module_iter_all():
        for module in ['core', 'apps']:
            list(module_iter(module=module, module_prefix='model'))


environment = Environment()
