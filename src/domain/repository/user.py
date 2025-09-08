from abc import ABC, abstractmethod

from src.infrastructure.db.user.user_table import UserTable


class UserRepository(ABC):
    entity_cls: type[UserTable] = UserTable

    @abstractmethod
    def get_by_email(self, email: str) -> UserTable | None:
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
    ) -> UserTable:
        raise NotImplementedError

    @abstractmethod
    def upsert_google_identity(
        self, *, email: str, name: str | None, sub: str, picture: str | None
    ) -> UserTable:
        """Find existing user by email or create one. Update provider/sub/picture as needed."""
        raise NotImplementedError
