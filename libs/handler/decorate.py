from typing import List, Union


class HandlerDecorate(object):

    def __init__(self, paths: Union[str, List[str]], hosts: Union[str, List[str]] = None, index: int = 0):
        self.__handler_paths__ = paths if isinstance(paths, List) else [paths]
        self.__handler_hosts__ = hosts if isinstance(hosts, List) else [hosts] if hosts is not None else []
        self.__handler_index__ = index

    def __call__(self, cls):
        cls.__handler_paths__ = self.__handler_paths__
        cls.__handler_hosts__ = self.__handler_hosts__
        cls.__handler_index__ = self.__handler_index__
        return cls
