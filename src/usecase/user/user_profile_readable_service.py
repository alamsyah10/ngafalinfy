from abc import ABC, abstractmethod

from src.usecase.user.user_profile_schema import (
    UserProfileResponse,
    UserSettingsResponse,
)


class UserProfileReadableService(ABC):
    @abstractmethod
    def find_profile_by_user_id(self, user_id: int) -> UserProfileResponse | None:
        raise NotImplementedError

    @abstractmethod
    def find_settings_by_user_id(self, user_id: int) -> UserSettingsResponse | None:
        raise NotImplementedError
