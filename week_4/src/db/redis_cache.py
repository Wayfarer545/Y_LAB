from typing import NoReturn, Optional, Union, Tuple, Dict, ByteString
from datetime import timedelta

from src.core import config
from src.db import AbstractCache


__all__ = ("UserCache", "PostCache")


class UserCache(AbstractCache):
    def get(self, key: str) -> Optional[Dict]:
        return self.cache.get(name=key)

    def set(
        self,
        key: str,
        value: Union[ByteString, str],
        expire: int = config.CACHE_EXPIRE_IN_SECONDS
        ):
        self.cache.set(name=key, value=value, ex=expire)

    def remove(self, key: str):
        self.cache.delete(key)

    def add_token(self, key: str, value: str):
        self.cache.sadd(key, value)

    def set_expiration_time(self, key: str, expire: timedelta):
        self.cache.expire(name=key, time=expire)

    def get_tokens(self, key: str) -> Tuple[ByteString]:
        return self.cache.smembers(key)

    def delete_token(self, key: str, value: str):
        self.cache.srem(key, 1, value)

    def close(self):
        self.cache.close()


class PostCache(AbstractCache):
    def get(self, key: str) -> Optional[Dict]:
        return self.cache.get(name=key)

    def set(
        self,
        key: str,
        value: Union[ByteString, str],
        expire: int = config.CACHE_EXPIRE_IN_SECONDS
        ):
        self.cache.set(name=key, value=value, ex=expire)

    def remove(self, key: str):
        self.cache.delete(key)

    def close(self):
        self.cache.close()