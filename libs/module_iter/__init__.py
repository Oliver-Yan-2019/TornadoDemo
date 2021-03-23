import pkgutil
import importlib


def module_iter(module: any, module_prefix: str = ''):
    """遍历package下所有的模块, 根据module前缀过滤module列表

    >>> [_.__name__ for _ in module_iter('libs')]
    ['libs.handler.decorate', 'libs.handler.factory']

    Args:
        module: 包
        module_prefix: module前缀

    Returns:

    """

    module = importlib.import_module(module) if isinstance(module, str) else module
    module_path = module.__path__[0]
    module_name = module.__name__

    module_stack = []
    while True:
        for _, name, is_package in pkgutil.walk_packages([module_path]):
            sub_module_name = f'{module_name}.{name}'
            if is_package is False:
                if not name.startswith(module_prefix):
                    continue

                yield importlib.import_module(sub_module_name)
            else:
                module_stack.append((f'{module_path}/{name}', sub_module_name))

        if not module_stack:
            break
        else:
            module_path, module_name = module_stack.pop()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
