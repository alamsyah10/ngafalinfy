from typing import Literal

from pydantic import Field

from src.domain.model.common import CustomBaseModel
from src.domain.model.user.user import User


class CreateUserRequest(CustomBaseModel):
    email: str = Field(examples=["test@gmail.com"], description="User email")
    display_name: str = Field(examples=["Tester"], description="User display name")
    provider: str = Field(examples=["Google"], description=["User account provider"])


class AuthUserResponse(CustomBaseModel):
    id: int = Field(examples=[1], description="Authenticated")
    email: str
    display_name: str | None = None
    picture_url: str | None = None

    @classmethod
    def from_entity(cls, user: User) -> "AuthUserResponse":
        return cls(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            picture_url=user.picture_url,
        )


class AuthTokenResponse(CustomBaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: AuthUserResponse

    @classmethod
    def from_parts(
        cls, access_token: str, token_type: Literal["bearer"], user: AuthUserResponse
    ) -> "AuthTokenResponse":
        return cls(access_token=access_token, token_type=token_type, user=user)


class LogoutResponse(CustomBaseModel):
    message: str

    @classmethod
    def from_parts(cls, message) -> "LogoutResponse":
        return cls(message=message)
