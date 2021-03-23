from threading import Lock

_lock = Lock()


def singleton(cls):
    """线程安全的单例

    Args:
        cls: 类

    Returns:

    """

    instances = {}

    def _singleton(*args, **kwargs):
        def create_new(*new_args, **new_kwargs):
            if _lock.acquire():
                if cls not in instances:
                    instances[cls] = cls(*new_args, **new_kwargs)

                _lock.release()
                return instances[cls]

        if cls not in instances:
            return create_new(*args, **kwargs)

        return instances[cls]

    return _singleton


__all__ = [
    'singleton'
]

if __name__ == '__main__':
    @singleton
    class A(object):
        pass


    class B(object):
        pass


    from threading import Thread

    thread_1 = Thread(target=lambda: print(f'A:{id(A())}\n'))
    thread_2 = Thread(target=lambda: print(f'A:{id(A())}\n'))
    thread_1.start()
    thread_1.join(1)
    thread_2.start()
    thread_2.join(1)

    thread_3 = Thread(target=lambda: print(f'B:{id(B())}\n'))
    thread_4 = Thread(target=lambda: print(f'B:{id(B())}\n'))
    thread_3.start()
    thread_3.join(1)
    thread_4.start()
    thread_4.join(1)
