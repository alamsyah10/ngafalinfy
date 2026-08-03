from abc import ABC, abstractmethod

from src.domain.model.user.user_profile_exception import (
    UserProfileNotFoundError,
    UserSettingsNotFoundError,
)
from src.usecase.user.user_profile_readable_service import UserProfileReadableService
from src.usecase.user.user_profile_schema import (
    UserProfileResponse,
    UserSettingsResponse,
)


class UserProfileReadableUseCase(ABC):
    @abstractmethod
    def fetch_profile(self, user_id: int) -> UserProfileResponse:
        raise NotImplementedError

    @abstractmethod
    def fetch_settings(self, user_id: int) -> UserSettingsResponse:
        raise NotImplementedError


class UserProfileReadableUseCaseImpl(UserProfileReadableUseCase):
    def __init__(self, service: UserProfileReadableService):
        self.service = service

    def fetch_profile(self, user_id: int) -> UserProfileResponse:
        profile = self.service.find_profile_by_user_id(user_id)
        if profile is None:
            raise UserProfileNotFoundError(user_id)
        return profile

    def fetch_settings(self, user_id: int) -> UserSettingsResponse:
        settings = self.service.find_settings_by_user_id(user_id)
        if settings is None:
            raise UserSettingsNotFoundError(user_id)
        return settings
