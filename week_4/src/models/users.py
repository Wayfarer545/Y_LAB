from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel

__all__ = ("Account",)


class Account(SQLModel, table=True):
    uuid: str = Field(nullable=False, primary_key=True)
    username: str = Field(nullable=False, primary_key=True)
    email: str = Field(nullable=False, primary_key=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(
        nullable=False, default=datetime.now(tz=timezone.utc))
    roles: str = Field(nullable=False, default="simple")
    is_active: bool = Field(nullable=False, default=True)
    is_superuser: bool = Field(nullable=False, default=False)
    is_totp_enabled: bool = Field(nullable=False, default=False)
