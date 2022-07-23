from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Dict, Optional


__all__ = (
    "AccountInfo",
    "User",
    "SignupRequest",
    "SignupResponse",
    "LoginForm",
    "LoginResponse",
    "RefreshResponse",
    "UpdateRequest",
    "UpdateResponse",
    "DefaultResponse",
    "RefreshMatrix",
    "AccessMatrix"
    )

class DefaultResponse(BaseModel):
    msg: str


class AccountInfo(BaseModel):
    uuid: str
    username: str
    email: str
    is_superuser: bool
    created_at: datetime
    roles: str


class User(AccountInfo):
    is_totp_enabled: bool
    is_active: bool


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class SignupResponse(DefaultResponse):
    user: User


class LoginForm(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshResponse(LoginResponse):
    ...


class UpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UpdateResponse(DefaultResponse):
    user: User
    access_token: str


class RefreshMatrix(BaseModel):
    fresh: bool = True
    iat: Optional[int] = None
    type: str = "undefined"
    uuid: str
    exp: Optional[int] = None


class AccessMatrix(RefreshMatrix):
    jti: Optional[int] = None
    nbf: Optional[int] = None
    refresh_uuid: Optional[str] = None
    username: str
    email: str
    is_superuser: bool
    created_at: datetime
    roles: str