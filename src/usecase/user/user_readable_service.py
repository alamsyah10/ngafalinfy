from abc import ABC, abstractmethod

from src.usecase.user.user_schema import AuthUserResponse


class UserReadableService(ABC):
    """
    UserReadableService defines a query service interface related User entity.
    """

    @abstractmethod
    def find_by_id(self, user_id: int) -> AuthUserResponse | None:
        raise NotImplementedError
