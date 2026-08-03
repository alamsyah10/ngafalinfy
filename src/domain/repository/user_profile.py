from abc import ABC, abstractmethod

from src.domain.model.user.user_profile import UserProfile


class UserProfileRepository(ABC):
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> UserProfile | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, profile: UserProfile) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, profile: UserProfile) -> None:
        raise NotImplementedError
