from abc import ABC, abstractmethod
from typing import Optional, Union, ByteString

from redis import Redis

from src.core import config
from src.core import config

__all__ = (
    "AbstractCache",
    "get_post_cache",
    "get_active_cache",
    "get_blocked_cache"
    )


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(
        self,
        key: str,
        value: Union[ByteString, str],
        expire: int = config.CACHE_EXPIRE_IN_SECONDS,
    ):
        pass

    @abstractmethod
    def remove(self, key: str):
        pass

    @abstractmethod
    def close(self):
        pass


posts_cache: Optional[AbstractCache] = None
active_tokens: Optional[AbstractCache] = None
blocked_tokens: Optional[AbstractCache] = None


def get_post_cache() -> AbstractCache:
    return posts_cache

def get_active_cache() -> AbstractCache:
    return active_tokens

def get_blocked_cache() -> AbstractCache:
    return blocked_tokens

