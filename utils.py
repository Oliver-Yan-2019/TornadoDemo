class Obj(object):
    def __init__(self, d):
        new_d = {}
        for a, b in list(d.items()):
            if isinstance(b, (list, tuple)):
                new_d[a] = [Obj(x) if isinstance(x, (list, tuple, dict)) else x for x in b]
            elif isinstance(b, dict):
                new_d[a] = Obj(b)
            else:
                new_d[a] = b

        self.__dict__ = new_d

    @property
    def json(self):
        value = {}
        for k, v in list(self.__dict__.items()):
            value[k] = v.json if isinstance(v, Obj) else [
                v_k.json if isinstance(v_k, Obj) else v_k for v_k in v
            ] if isinstance(v, list) else v

        return value

    @property
    def keys(self):
        return list(self.__dict__.keys())

    def get(self, key):
        """
        根据key值获取对象
        :param key:
        :return:
        """
        return self.__dict__.get(key)
