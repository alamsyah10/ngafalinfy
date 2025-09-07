from abc import ABC, abstractmethod

from src.infrastructure.db.user.user_table import User


class UserRepository(ABC):
    entity_cls: type[User] = User

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        *,
        email: str,
        display_name: str | None,
        picture_url: str | None,
        provider: str | None,
        provider_sub: str | None,
        is_active: bool = True,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    def upsert_google_identity(
        self, *, email: str, name: str | None, sub: str, picture: str | None
    ) -> User:
        """Find existing user by email or create one. Update provider/sub/picture as needed."""
        raise NotImplementedError
