from abc import ABC, abstractmethod

from src.domain.model.user.user_profile import UserProfile
from src.domain.model.user.user_settings import UserSettings
from src.domain.repository.user_profile import UserProfileRepository
from src.domain.repository.user_settings import UserSettingsRepository
from src.usecase.user.user_profile_schema import (
    UpdateProfileRequest,
    UpdateSettingsRequest,
    UserProfileResponse,
    UserSettingsResponse,
)


class UserProfileWriteableUseCaseUnitOfWork(ABC):
    profile_repository: UserProfileRepository
    settings_repository: UserSettingsRepository

    @abstractmethod
    def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class UserProfileWriteableUseCase(ABC):
    @abstractmethod
    def get_or_create_profile(self, user_id: int) -> UserProfileResponse:
        raise NotImplementedError

    @abstractmethod
    def update_profile(
        self, user_id: int, req: UpdateProfileRequest
    ) -> UserProfileResponse:
        raise NotImplementedError

    @abstractmethod
    def get_or_create_settings(self, user_id: int) -> UserSettingsResponse:
        raise NotImplementedError

    @abstractmethod
    def update_settings(
        self, user_id: int, req: UpdateSettingsRequest
    ) -> UserSettingsResponse:
        raise NotImplementedError


class UserProfileWriteableUseCaseImpl(UserProfileWriteableUseCase):
    def __init__(self, uow: UserProfileWriteableUseCaseUnitOfWork):
        self.uow = uow

    def get_or_create_profile(self, user_id: int) -> UserProfileResponse:
        profile = self.uow.profile_repository.find_by_user_id(user_id)
        if profile is None:
            profile = UserProfile.default_for(user_id)
            try:
                self.uow.begin()
                self.uow.profile_repository.create(profile)
                self.uow.commit()
                profile = self.uow.profile_repository.find_by_user_id(user_id)
                assert profile is not None
            except Exception:
                self.uow.rollback()
                raise
        return _profile_to_response(profile)

    def update_profile(
        self, user_id: int, req: UpdateProfileRequest
    ) -> UserProfileResponse:
        profile = self.uow.profile_repository.find_by_user_id(user_id)
        if profile is None:
            profile = UserProfile.default_for(user_id)
            try:
                self.uow.begin()
                self.uow.profile_repository.create(profile)
                self.uow.commit()
                profile = self.uow.profile_repository.find_by_user_id(user_id)
                assert profile is not None
            except Exception:
                self.uow.rollback()
                raise

        updated = profile.update(
            bio=req.bio,
            avatar_url=req.avatar_url,
            phone=req.phone,
            location=req.location,
            website=req.website,
        )
        try:
            self.uow.begin()
            self.uow.profile_repository.update(updated)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise
        return _profile_to_response(updated)

    def get_or_create_settings(self, user_id: int) -> UserSettingsResponse:
        settings = self.uow.settings_repository.find_by_user_id(user_id)
        if settings is None:
            settings = UserSettings.default_for(user_id)
            try:
                self.uow.begin()
                self.uow.settings_repository.create(settings)
                self.uow.commit()
                settings = self.uow.settings_repository.find_by_user_id(user_id)
                assert settings is not None
            except Exception:
                self.uow.rollback()
                raise
        return _settings_to_response(settings)

    def update_settings(
        self, user_id: int, req: UpdateSettingsRequest
    ) -> UserSettingsResponse:
        settings = self.uow.settings_repository.find_by_user_id(user_id)
        if settings is None:
            settings = UserSettings.default_for(user_id)
            try:
                self.uow.begin()
                self.uow.settings_repository.create(settings)
                self.uow.commit()
                settings = self.uow.settings_repository.find_by_user_id(user_id)
                assert settings is not None
            except Exception:
                self.uow.rollback()
                raise

        updated = settings.update(
            language=req.language,
            timezone=req.timezone,
            theme=req.theme,
            daily_review_goal=req.daily_review_goal,
            notifications_enabled=req.notifications_enabled,
        )
        try:
            self.uow.begin()
            self.uow.settings_repository.update(updated)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise
        return _settings_to_response(updated)


def _profile_to_response(profile: UserProfile) -> UserProfileResponse:
    return UserProfileResponse(
        id=profile.id or 0,
        user_id=profile.user_id,
        bio=profile.bio,
        avatar_url=profile.avatar_url,
        phone=profile.phone,
        location=profile.location,
        website=profile.website,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


def _settings_to_response(settings: UserSettings) -> UserSettingsResponse:
    return UserSettingsResponse(
        id=settings.id or 0,
        user_id=settings.user_id,
        language=settings.language,
        timezone=settings.timezone,
        theme=settings.theme,
        daily_review_goal=settings.daily_review_goal,
        notifications_enabled=settings.notifications_enabled,
        created_at=settings.created_at,
        updated_at=settings.updated_at,
    )
