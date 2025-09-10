from abc import ABC, abstractmethod

from src.domain.model.user.user import User


class UserRepository(ABC):
    """
    UserRepository defines a repository interface for User entity.
    """

    @abstractmethod
    def get_by_email(self, email: str):
        raise NotImplementedError

    @abstractmethod
    def create(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def upsert_google_identity(
        self, *, email: str, name: str | None, sub: str, picture: str | None
    ):
        raise NotImplementedError
