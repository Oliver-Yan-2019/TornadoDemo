from functools import wraps

from core.cache.redis_cache.service import RedisService
from environment import environment as env
from libs.error import SUBCLASS_ILLEGAL
from core.base.model import BaseModel


class RedisCache(object):
    def __init__(self, key, source, cache_type='json'):
        self.key = key
        self.source = source
        self.cache_type = cache_type
        self.expire = env.conf.get_conf('redis', 'default_expire_time', conf_type=int, fallback=24 * 60 * 60)

    def __call__(self, origin_func):
        @wraps(origin_func)
        def new_fun(*args, **kwargs):
            cls = args[0]
            if not issubclass(cls, BaseModel):
                raise SUBCLASS_ILLEGAL.description('该方法所属类必须为BaseModel子类')

            cache_key = f'{self.key}:{args[1]}'
            if RedisService.exists(cache_key):
                cache_value = self.get_cache(cache_key)
            else:
                cache_value = origin_func(*args, **kwargs)
                self.set_cache(cache_key, cache_value)

            return cache_value

        return new_fun

    def get_cache(self, key):
        if self.cache_type == 'json':
            value = RedisService.get_json(key)
        elif self.cache_type == 'hash':
            value = RedisService.hash_get_all(key)
        elif self.cache_type == 'list':
            value = RedisService.get_list(key)
        else:
            value = RedisService.get(key)

        RedisService.expire(key, self.expire)
        return value

    def set_cache(self, key, value):
        if self.cache_type == 'json':
            RedisService.set_json(key, value, self.expire)
        elif self.cache_type == 'hash':
            RedisService.hash_multi_set(key, value, self.expire)
        elif self.cache_type == 'list':
            RedisService.set_list(key, value, self.expire)
        else:
            RedisService.set(key, value, self.expire)


redis_cache = RedisCache
