from os.path import join, dirname
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool
from redis import StrictRedis
from logging import basicConfig

from libs.handler.factory import HandlerFactory
from libs.singleton import singleton
from libs.config import Config
from libs.module_iter import module_iter

BASE_DIR = dirname(__file__)


@singleton
class Environment(object):
    def __init__(self):
        """应用运行环境, 单例"""

        self.is_inited = False  # 单例, 初始化一次即可
        self.conf = Config()  # 配置工具
        self.db_engine = None  # 数据库引擎
        self.db_session = None  # 数据库会话
        self.rd_client = None  # Redis客户端

    def initialize(self):
        """应用环境初始化

        Returns:

        """

        if self.is_inited is True:
            return

        self.init_config()
        self.init_database()
        self.init_redis()
        self.module_iter_all()

    def init_config(self):
        """初始化配置

        Returns:

        """

        for file_name in ['default', 'product', 'develop']:
            self.conf.initialize(join(BASE_DIR, 'config', f'{file_name}.conf'))

    def init_database(self):
        """初始化数据库

        Returns:

        """

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

    def init_redis(self):
        """初始化Redis

        Returns:

        """

        self.rd_client = StrictRedis.from_url(
            url=self.conf.get_conf('redis', 'url'),
            db=self.conf.get_conf('redis', 'db', conf_type=int, fallback=0),
            client_name=self.conf.get_conf('redis', 'name', fallback='default'),
            health_check_interval=self.conf.get_conf('redis', 'health_check_interval', conf_type=int, fallback=30),
            decode_responses=self.conf.get_conf('redis', 'decode_responses', conf_type=bool, fallback=True),
        )

    def init_logging(self):
        """初始化日志服务

        Returns:

        """

        basicConfig(
            format='%(thread)d [%(filename)s:%(lineno)d] %(message)s',
            level=self.conf.get_conf('logging', 'level', conf_type='INFO'),
        )

    @staticmethod
    def get_handlers():
        """获取路由处理器

        Returns:

        """

        handler_factory = HandlerFactory(module_libs=['core', 'apps'])
        return handler_factory.get_handlers()

    def get_tornado_settings(self):
        """获取Tornado配置

        Returns:

        """

        return dict(
            static_path=join(BASE_DIR, "statics"),
            # static_url_prefix="/server/static/",
            template_path=join(BASE_DIR, "templates"),
            # cookie_secret=self.conf.get_conf('tornado', 'cookie_secret'),
            # gzip=self.conf.get_conf('tornado', 'gzip', conf_type=bool),
            debug=self.conf.get_conf('tornado', 'debug', conf_type=bool)
        )

    @staticmethod
    def module_iter_all():
        """加载所有模块

        Returns:

        """

        for module in ['core', 'apps']:
            list(module_iter(module=module, module_prefix='model'))


environment = Environment()
