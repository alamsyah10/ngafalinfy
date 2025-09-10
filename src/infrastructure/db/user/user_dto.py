from src.domain.model.user.user import User
from src.infrastructure.db.user.user_table import UserTable
from src.usecase.user.user_schema import AuthUserResponse


class UserDTO(UserTable):
    """
    UserDTO is a data transfer object associated with User entity.
    """

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
