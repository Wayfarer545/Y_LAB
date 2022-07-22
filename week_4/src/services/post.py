import json
from functools import lru_cache
from typing import Optional, Dict

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas import PostCreate, PostModel
from src.db import AbstractCache, get_post_cache, get_session
from src.models import Post
from src.services import ServiceMixin

__all__ = ("PostService", "get_post_service")


class PostService(ServiceMixin):
    def get_post_list(self) -> Dict:
        """Получить список постов."""
        posts = self.session.query(Post).order_by(Post.created_at).all()
        return {"posts": [PostModel(**post.dict()) for post in posts]}

    def get_post_detail(self, item_id: int) -> Optional[Dict]:
        """Получить детальную информацию поста."""
        if cached_post := self.cached_posts.get(key=f"{item_id}"):
            return json.loads(cached_post)

        post: Post = self.session.query(
            Post).filter(Post.id == item_id).first()
        if post:
            self.cached_posts.set(key=f"{post.id}", value=post.json())
            self.cached_posts.remove(f"{post.id}")
        return post.dict() if post else None

    def create_post(self, post: PostCreate, author: str) -> Dict:
        """Создать пост."""
        new_post = Post(
            title=post.title,
            description=post.description,
            author=author
            )
        self.session.add(new_post)
        self.session.commit()
        self.session.refresh(new_post)
        return new_post.dict()


# get_post_service — это провайдер PostService. Синглтон
@lru_cache()
def get_post_service(
    cache: AbstractCache = Depends(get_post_cache),
    session: Session = Depends(get_session),
) -> PostService:
    return PostService(cached_posts=cache, session=session)
