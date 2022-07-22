from http import HTTPStatus
from typing import Optional, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.api.v1.schemas import PostCreate, PostListResponse, PostModel
from src.services import (
    PostService,
    UserService,
    get_post_service,
    get_user_service
    )


router = APIRouter()


@router.get(
    path="/",
    response_model=PostListResponse,
    summary="Список постов",
    tags=["posts"],
    )
def post_list(
    post_service: PostService = Depends(get_post_service),
    ) -> PostListResponse:
    posts: Dict = post_service.get_post_list()
    if not posts:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="posts not found")
    return PostListResponse(**posts)


@router.get(
    path="/{post_id}",
    response_model=PostModel,
    summary="Получить определенный пост",
    tags=["posts"],
    )
def post_detail(
    post_id: int, post_service: PostService = Depends(get_post_service),
    ) -> PostModel:
    post: Optional[Dict] = post_service.get_post_detail(item_id=post_id)
    if not post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="post not found")
    return PostModel(**post)


@router.post(
    path="/",
    response_model=PostModel,
    summary="Создать пост",
    tags=["posts"],
    )
def post_create(
        post: PostCreate,
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
        post_service: PostService = Depends(get_post_service),
        user_service: UserService = Depends(get_user_service)
    ) -> PostModel:
    user_data: Dict = user_service.token_validation(token)
    post: Dict = post_service.create_post(
        post=post,
        author=user_data["username"]
    )
    return PostModel(**post)

