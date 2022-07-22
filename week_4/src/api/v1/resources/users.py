from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.api.v1.schemas import *
from src.services import UserService, get_user_service
from src.models.users import Account

router = APIRouter()


@router.post(
    path="/signup",
    response_model=SignupResponse,
    summary="Регистрация на сайте",
    tags=["users"],
    )
def signup(
    user: SignupRequest,
    user_service: UserService = Depends(get_user_service),
    ) -> SignupResponse:
    new_user: Dict = user_service.create_new_user(user=user)
    return SignupResponse(msg="successful", user=User(**new_user))


@router.post(
    path="/login",
    response_model=LoginResponse,
    summary="Вход на сайт",
    tags=["users"]
    )
def login(
        credentials: LoginForm,
        user_service: UserService = Depends(get_user_service)):
    access, refresh = user_service.sign_in(credentials)
    return LoginResponse(access_token=access, refresh_token=refresh)


@router.post(
    path="/refresh",
    response_model=RefreshResponse,
    summary="Обновление токена",
    tags=["users"]
    )
def refresh_token(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
        user_service: UserService = Depends(get_user_service)):
    access, refresh = user_service.refresh_token(token)
    return RefreshResponse(access_token=access, refresh_token=refresh)


@router.get(
    path="/users/me",
    response_model=AccountInfo,
    summary="Просмотр профиля",
    tags=["account"]
    )
def show_account(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
        user_service: UserService = Depends(get_user_service)):
    account_info = user_service.account_info(token)
    return AccountInfo(**account_info)


@router.patch(
    path="/users/me",
    response_model=UpdateResponse,
    summary="Обновление профиля",
    tags=["account"]
    )
def update_account(
        user_data: UpdateRequest,
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
        user_service: UserService = Depends(get_user_service)):
    response = user_service.patch_account(token, user_data)
    return UpdateResponse(**response)


@router.post(
    path="/logout",
    response_model=DefaultResponse,
    summary="Выход из аккаунта",
    tags=["users"]
    )
def logout(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
        user_service: UserService = Depends(get_user_service)):
    user_service.logout(token)
    return {"msg": "You have been logged out."}


@router.post(
    path="/logout_all",
    response_model=DefaultResponse,
    summary="Выход на всех устройствах",
    tags=["users"]
    )
def logout_all(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
        user_service: UserService = Depends(get_user_service)):
    user_service.full_logout(token)
    return {"msg": "You have been logged out from all devices."}