from typing import Optional

from sqlmodel import Session

from src.db import AbstractCache


class ServiceMixin:
    def __init__(self,
                 session: Session,
                 cached_posts: Optional[AbstractCache] = None,
                 cached_active_tokens: Optional[AbstractCache] = None,
                 cached_blocked_tokens: Optional[AbstractCache] = None,
                 ):
        self.cached_posts: AbstractCache = cached_posts
        self.cached_active_tokens: AbstractCache = cached_active_tokens
        self.cached_blocked_tokens: AbstractCache = cached_blocked_tokens
        self.session: Session = session
