from dataclasses import dataclass

from src.domain.model.auth import AuthUserResponse
from src.infrastructure.db.user.user_table import User


@dataclass
class UserDTO:
    id: int
    email: str
    display_name: str | None
    picture_url: str | None
    provider: str | None
    provider_sub: str | None
    is_active: bool

    @classmethod
    def from_entity(cls, entity: User) -> "UserDTO":
        return cls(
            id=entity.id,
            email=entity.email,
            display_name=entity.display_name,
            picture_url=entity.picture_url,
            provider=entity.provider,
            provider_sub=entity.provider_sub,
            is_active=entity.is_active,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            display_name=self.display_name,
            picture_url=self.picture_url,
            provider=self.provider,
            provider_sub=self.provider_sub,
            is_active=self.is_active,
        )

    def to_auth_user(self) -> AuthUserResponse:
        return AuthUserResponse(
            id=self.id,
            email=self.email,
            display_name=self.display_name,
            picture_url=self.picture_url,
        )
