from inspect import getmembers, isclass
from tornado.util import import_object
from tornado.web import url

from libs.module_iter import module_iter


class HandlerFactory(object):
    def __init__(self, module_libs: list):
        self.handler_libs = self.get_handler_libs(module_libs)

    def __get_handlers_by_host(self, host: str = None):
        handlers = []
        for handler in self.handler_libs:
            if not (host is None and handler['hosts'] == []) or (host and host in handler['hosts']):
                continue

            paths = handler.get('paths')
            handlers.extend([url(path, import_object(handler.get('name'))) for path in paths])

        return handlers

    def get_handlers(self):
        host_set = set()
        for handler in self.handler_libs:
            for host in handler.get('hosts'):
                host_set.add(host)

        return self.__get_handlers_by_host(), [[host, self.__get_handlers_by_host(host)] for host in host_set]

    @staticmethod
    def get_handler_libs(module_libs: list):
        handler_libs = []

        for module in module_libs:
            for sub_module in module_iter(module, module_prefix='handler'):
                handler_libs.extend([
                    dict(
                        paths=cls.__handler_paths__,
                        index=cls.__handler_index__,
                        name=f'{cls.__module__}.{cls.__name__}',
                        hosts=cls.__handler_hosts__
                    ) for _, cls in getmembers(sub_module, isclass) if hasattr(cls, '__handler_paths__')
                ])

        handler_libs.sort(key=lambda handler: handler['index'])

        return handler_libs
