from typing import Literal

from pydantic import BaseModel


class AuthUserResponse(BaseModel):
    id: int
    email: str
    display_name: str | None = None
    picture_url: str | None = None


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: AuthUserResponse


class LogoutResponse(BaseModel):
    message: str
