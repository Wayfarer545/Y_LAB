import json
import os
from uuid import uuid4
from functools import lru_cache
from typing import Optional, Union, Tuple, Dict
from datetime import timedelta, datetime, timezone

import jose
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session, select
from jose import jwt
from jose.jwt import ExpiredSignatureError, JWTError

from src.api.v1.schemas import *
from src.db import (
    AbstractCache,
    get_active_cache,
    get_blocked_cache,
    get_session
    )
from src.models import Account
from src.services import ServiceMixin
from src.core import JWT_SECRET_KEY, JWT_ALGORITHM


__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):
    def create_new_user(self, user: SignupRequest) -> Dict:
        """Регистрация нового пользователя."""
        new_user = Account(
            uuid=str(uuid4()),
            username=user.username,
            email=user.email,
            password=self.get_pwd_hash(user.password)
        )
        self.user_existance_check(user)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.dict()

    def sign_in(self, creds: LoginForm) -> Tuple[str, str]:
        """Аутентификация."""
        user: Account = self.session.exec(
            select(Account).where(
                Account.username == creds.username)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Incorrect username.")

        if not self.verify_pwd(creds.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Incorrect password.")
        return self.create_tokens(user)

    def refresh_token(self, refresh_token: str):
        """Обновление токена."""
        payload = self.token_validation(refresh_token)
        cached_tokens = self.cached_active_tokens.get_tokens(payload['uuid'])
        for token in cached_tokens:
            if token.decode('utf-8') == refresh_token:
                user = self.session.exec(
                    select(Account).where(
                        Account.uuid == payload["uuid"])).first()
                return self.create_tokens(user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    def account_info(self, token: str) -> Dict:
        """Получить детальную информацию о пользователе."""
        payload = self.token_validation(token)
        response_data = self.session.exec(
            select(Account).where(
                Account.uuid == payload["uuid"])).first()
        return response_data.dict()

    def patch_account(self, token: str, data: UpdateRequest) -> Dict:
        """Обновление информации профиля."""
        payload: Dict = self.token_validation(token)
        self.user_existance_check(data)
        old_data: Account = self.session.exec(
            select(Account).where(
                Account.uuid == payload["uuid"])).first()

        old_data.username = data.username
        old_data.email = data.email
        self.session.commit()
        self.session.refresh(old_data)
        self.cached_blocked_tokens.set(payload["jti"], '', 900)
        access_token: str = self.create_access_token(old_data)

        return {
            "msg": "Update is successful. Please use new access_token",
            "user": User(**old_data.dict()),
            "access_token": access_token
            }

    def logout(self, token: str):
        """Выход из аккаунта."""
        payload: Dict = self.token_validation(token)
        self.cached_blocked_tokens.set(payload["jti"], '', 900)

    def full_logout(self, token: str):
        """Выйти со всех устройств"""
        payload: dict = self.token_validation(token)
        self.cached_active_tokens.remove(payload["uuid"])
        self.cached_blocked_tokens.set(payload["jti"], "", 900)

    def token_validation(self, token: str = None) -> Dict:
        """Проверка подлинности токена.

        Включает проверку шифрования, валидацию по сроку истечения
        и наличие токена в кэщ-базе заблокированных для типа Access.
        """
        try:
            payload: Dict = jwt.decode(
                token,
                JWT_SECRET_KEY,
                JWT_ALGORITHM
                )
            if payload["uuid"] is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Token invalid")

        if payload["type"] == "access":
            is_blocked: bytes = self.cached_blocked_tokens.get(payload["jti"])
            if is_blocked != None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return payload

    def user_existance_check(
            self,
            user: Union[SignupRequest, UpdateRequest]
            ) -> Tuple[str, str]:
        """Проверка наличия имени username или email в базе."""
        email_check = self.session.exec(
            select(Account).where(
                Account.email == user.email)).first()
        user_check = self.session.exec(
            select(Account).where(
                Account.username == user.username)).first()

        if email_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user.email} already exists")
        if user_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with username {user.username} already exists")

    def create_tokens(self, user_data: Dict) -> Tuple[str, str]:
        """Хаб-метод генерации пары токенов."""
        access: str = self.create_access_token(user_data)
        refresh: str = self.create_refresh_token(user_data)
        return access, refresh

    def create_access_token(self, user_data: Account) -> str:
        """Метод генерации access token"""
        matrix = AccessMatrix(**user_data.dict())
        matrix.type = "access"
        matrix.iat = datetime.timestamp(datetime.now(tz=timezone.utc))
        matrix.exp = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
        matrix.created_at = matrix.created_at.isoformat()
        matrix.jti = str(uuid4())
        matrix.nbf = matrix.iat
        matrix.refresh_uuid = matrix.jti

        return jwt.encode(matrix.dict(), JWT_SECRET_KEY, JWT_ALGORITHM)

    def create_refresh_token(self, user_data: Account) -> str:
        """Метод генерации refresh token"""
        matrix = RefreshMatrix(**user_data.dict())
        matrix.type = "refresh"
        matrix.iat = datetime.timestamp(datetime.now(tz=timezone.utc))
        matrix.exp = datetime.now(tz=timezone.utc) + timedelta(minutes=60)
        token = jwt.encode(matrix.dict(), JWT_SECRET_KEY, JWT_ALGORITHM)

        self.cached_active_tokens.add_token(matrix.uuid, token)
        self.cached_active_tokens.set_expiration_time(
            matrix.uuid,
            timedelta(minutes=60)
            )
        return token

    @staticmethod
    def get_pwd_hash(password: str):
        """Хеширование пароля"""
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.hash(password)

    @staticmethod
    def verify_pwd(password: str, hashed_pwd: bytes) -> bool:
        """Проверка подлинности пароля."""
        status = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return status.verify(password, hashed_pwd)



@lru_cache()
def get_user_service(
        active_cache: AbstractCache = Depends(get_active_cache),
        blocked_cache: AbstractCache = Depends(get_blocked_cache),
        session: Session = Depends(get_session),
        ) -> UserService:

    return UserService(cached_active_tokens=active_cache,
                       cached_blocked_tokens=blocked_cache,
                       session=session)

