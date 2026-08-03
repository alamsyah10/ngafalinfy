from abc import ABC, abstractmethod

from src.domain.model.user.user_settings import UserSettings


class UserSettingsRepository(ABC):
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> UserSettings | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, settings: UserSettings) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, settings: UserSettings) -> None:
        raise NotImplementedError
