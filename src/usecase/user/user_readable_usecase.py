from abc import ABC, abstractmethod

from src.domain.error.base import UserNotFoundError
from src.usecase.user.user_readable_service import UserReadableService
from src.usecase.user.user_schema import AuthUserResponse


class UserReadableUseCase(ABC):
    """
    UserReadableUseCase defines a query usecase interface related User entity.
    """

    @abstractmethod
    def fetch_user(self, id: int) -> AuthUserResponse:
        raise NotImplementedError


class UserReadableUseCaseImpl(UserReadableUseCase):
    """
    UserReadableUseCaseImpl implements a query usecases related User entity.
    """

    def __init__(self, user_service: UserReadableService):
        self.user_service: UserReadableService = user_service

    def fetch_user(self, id: int) -> AuthUserResponse:
        try:
            user = self.user_service.find_by_id(id)
            if user is None:
                raise UserNotFoundError(id)
        except:
            raise

        return user
