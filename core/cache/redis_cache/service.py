import orjson  # 性能比较好

from environment import environment as env


class RedisService(object):
    @classmethod
    def exists(cls, *keys):
        """批量检验键是否存在

        Args:
            *keys: 键列表

        Returns:

        """

        return env.rd_client.exists(*keys) == len(keys)

    @classmethod
    def expire(cls, key, seconds):
        """设置过期时间, 秒

        Args:
            key: 键
            seconds: 秒

        Returns:

        """

        env.rd_client.expire(key, seconds)

    @classmethod
    def set(cls, key, value, expire=None, p_expire=None, nx=None, xx=None):
        """设置字符键

        Args:
            key: 键
            value: 值
            expire: 过期时间, 秒
            p_expire: 过期时间, 毫秒
            nx: 如果这个键不存在则新增
            xx: 如果这个键存在则更新

        Returns:

        """

        env.rd_client.set(
            key, value,
            ex=expire,
            px=p_expire,
            nx=nx,
            xx=xx
        )

    @classmethod
    def get(cls, key):
        """获取键

        Args:
            key: 键
        Returns:

        """

        return env.rd_client.get(key)

    @classmethod
    def delete(cls, key):
        """删除键

        Args:
            key: 键

        Returns:

        """

        env.rd_client.delete(key)

    @classmethod
    def expires(cls, keys, seconds):
        """批量设置过期时间

        Args:
            keys: 键列表
            seconds: 过期时间, 秒

        Returns:

        """

        pipeline = env.rd_client.pipeline()
        for key in keys:
            pipeline.expire(key, seconds)

        pipeline.execute()

    @classmethod
    def multi_set(cls, mapping, seconds=None):
        """批量设置字符键

        Args:
            mapping: 字典
            seconds: 过期时间, 秒

        Returns:

        """

        env.rd_client.mset(mapping)
        if seconds is not None:
            cls.expires(mapping.keys(), seconds)

    @classmethod
    def multi_get(cls, keys):
        """批量获取键

        Args:
            keys: 键列表

        Returns:

        """

        pipeline = env.rd_client.pipeline()
        for key in keys:
            pipeline.get(key)

        return pipeline.execute()

    @classmethod
    def multi_delete(cls, keys):
        """批量删除键

        Args:
            keys: 键列表

        Returns:

        """

        pipeline = env.rd_client.pipeline()
        for key in keys:
            pipeline.delete(key)

        pipeline.execute()

    @classmethod
    def scan(cls, cursor=0, match=None, count=None, type_=None):
        """扫描键

        Args:
            cursor: 游标
            match: 正则匹配
            count: 扫描数量
            type_: 类型

        Returns:

        """

        _cursor, _list = env.rd_client.scan(
            cursor=cursor,
            match=match,
            count=count,
            _type=type_
        )
        return {'cursor': _cursor, 'list': _list}

    @classmethod
    def list_len(cls, key):
        """列表键长度

        Args:
            key: 键

        Returns:

        """

        return env.rd_client.llen(key)

    @classmethod
    def right_push(cls, key, item):
        """添加元素到列表尾部

        Args:
            key: 键
            item: 元素

        Returns:

        """

        env.rd_client.rpush(key, item)

    @classmethod
    def left_pop(cls, key):
        """从列表左侧删除元素

        Args:
            key: 键

        Returns:

        """

        return env.rd_client.lpop(key)

    @classmethod
    def block_left_pop(cls, key, timeout=0):
        """从列表左侧删除元素, 阻塞

        Args:
            key: 键
            timeout: 阻塞时长

        Returns:

        """

        return env.rd_client.blpop(key, timeout=timeout)

    @classmethod
    def hash_get_all(cls, key):
        """获取哈希键

        Args:
            key: 键

        Returns:

        """

        return env.rd_client.hgetall(key)

    @classmethod
    def hash_multi_set(cls, key, mapping, expire=None):
        """设置哈希键

        Args:
            key: 键
            mapping: 键值对映射
            expire: 过期时间, 秒

        Returns:

        """

        env.rd_client.hmset(key, mapping)
        if expire is not None:
            cls.expire(key, expire)

    """以下为常用API"""

    @classmethod
    def get_json(cls, key):
        """获取json

        Args:
            key: 键

        Returns:

        """

        value = cls.get(key)
        return None if value is None else orjson.loads(value)

    @classmethod
    def multi_get_json(cls, keys):
        """批量获取json

        Args:
            keys: 键列表

        Returns:

        """

        value_list = cls.multi_get(keys)
        json_list = []
        for value in value_list:
            json_list.append(None if value is None else orjson.loads(value))

        return json_list

    @classmethod
    def set_json(cls, key, json_, expire=None):
        """设置json

        Args:
            key: 键
            json_: json
            expire: 过期时间, 秒

        Returns:

        """

        value = orjson.dumps(json_)
        if expire is not None:
            cls.set(key, value, expire)

    @classmethod
    def multi_set_json(cls, json_mapping, seconds=None):
        """批量设置json

        Args:
            json_mapping: json映射
            seconds: 过期时间, 秒

        Returns:

        """

        mapping = {key: orjson.dumps(value) for key, value in json_mapping.items()}
        cls.multi_set(mapping, seconds)

    @classmethod
    def get_list(cls, key):
        """获取列表

        Args:
            key: 键

        Returns:

        """

        value = cls.get(key)
        return None if value is None else orjson.loads(value)

    @classmethod
    def set_list(cls, key, list_, expire=None):
        """设置列表

        Args:
            key: 键
            list_: 列表
            expire: 过期时间, 秒

        Returns:

        """

        value = orjson.dumps(list_)
        cls.set(key, value, expire)
