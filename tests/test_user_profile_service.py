from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.domain.model.user.user_profile import UserProfile
from src.domain.model.user.user_profile_exception import (
    UserProfileNotFoundError,
    UserSettingsNotFoundError,
)
from src.domain.model.user.user_settings import Language, UserSettings
from src.usecase.user.user_profile_readable_usecase import (
    UserProfileReadableUseCaseImpl,
)
from src.usecase.user.user_profile_schema import (
    UpdateProfileRequest,
    UpdateSettingsRequest,
    UserProfileResponse,
    UserSettingsResponse,
)
from src.usecase.user.user_profile_writeable_usecase import (
    UserProfileWriteableUseCaseImpl,
)

NOW = datetime(2026, 1, 1, 0, 0, 0)
USER_ID = 1


def _make_profile(id: int = 10) -> UserProfile:
    return UserProfile(
        id=id,
        user_id=USER_ID,
        bio="Hello",
        created_at=NOW,
        updated_at=NOW,
    )


def _make_settings(id: int = 20) -> UserSettings:
    return UserSettings(
        id=id,
        user_id=USER_ID,
        created_at=NOW,
        updated_at=NOW,
    )


def _make_profile_response(profile: UserProfile) -> UserProfileResponse:
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


def _make_settings_response(s: UserSettings) -> UserSettingsResponse:
    return UserSettingsResponse(
        id=s.id or 0,
        user_id=s.user_id,
        language=s.language,
        timezone=s.timezone,
        theme=s.theme,
        daily_review_goal=s.daily_review_goal,
        notifications_enabled=s.notifications_enabled,
        created_at=s.created_at,
        updated_at=s.updated_at,
    )


# ---------------------------------------------------------------------------
# UserProfileReadableUseCase
# ---------------------------------------------------------------------------


class TestUserProfileReadableUseCase:
    def test_fetch_profile_returns_response(self):
        service = MagicMock()
        service.find_profile_by_user_id.return_value = _make_profile_response(
            _make_profile()
        )
        uc = UserProfileReadableUseCaseImpl(service)

        result = uc.fetch_profile(USER_ID)

        assert result.user_id == USER_ID
        assert result.bio == "Hello"

    def test_fetch_profile_raises_when_not_found(self):
        service = MagicMock()
        service.find_profile_by_user_id.return_value = None
        uc = UserProfileReadableUseCaseImpl(service)

        with pytest.raises(UserProfileNotFoundError):
            uc.fetch_profile(USER_ID)

    def test_fetch_settings_returns_response(self):
        service = MagicMock()
        service.find_settings_by_user_id.return_value = _make_settings_response(
            _make_settings()
        )
        uc = UserProfileReadableUseCaseImpl(service)

        result = uc.fetch_settings(USER_ID)

        assert result.user_id == USER_ID
        assert result.language == Language.EN

    def test_fetch_settings_raises_when_not_found(self):
        service = MagicMock()
        service.find_settings_by_user_id.return_value = None
        uc = UserProfileReadableUseCaseImpl(service)

        with pytest.raises(UserSettingsNotFoundError):
            uc.fetch_settings(USER_ID)


# ---------------------------------------------------------------------------
# UserProfileWriteableUseCase
# ---------------------------------------------------------------------------


def _make_uow(profile: UserProfile | None = None, settings: UserSettings | None = None):
    uow = MagicMock()
    uow.profile_repository.find_by_user_id.return_value = profile
    uow.settings_repository.find_by_user_id.return_value = settings
    return uow


class TestUserProfileWriteableUseCase:
    def test_get_or_create_profile_returns_existing(self):
        existing = _make_profile()
        uow = _make_uow(profile=existing)
        uc = UserProfileWriteableUseCaseImpl(uow)

        result = uc.get_or_create_profile(USER_ID)

        assert result.user_id == USER_ID
        uow.profile_repository.create.assert_not_called()

    def test_get_or_create_profile_creates_when_missing(self):
        uow = _make_uow(profile=None)
        # after create, find returns a profile with id
        uow.profile_repository.find_by_user_id.side_effect = [None, _make_profile()]
        uc = UserProfileWriteableUseCaseImpl(uow)

        result = uc.get_or_create_profile(USER_ID)

        uow.profile_repository.create.assert_called_once()
        assert result.user_id == USER_ID

    def test_update_profile_updates_existing(self):
        existing = _make_profile()
        uow = _make_uow(profile=existing)
        uc = UserProfileWriteableUseCaseImpl(uow)
        req = UpdateProfileRequest(
            bio="Updated bio", avatar_url=None, phone=None, location=None, website=None
        )

        result = uc.update_profile(USER_ID, req)

        uow.profile_repository.update.assert_called_once()
        assert result.bio == "Updated bio"

    def test_get_or_create_settings_creates_when_missing(self):
        uow = _make_uow(settings=None)
        uow.settings_repository.find_by_user_id.side_effect = [None, _make_settings()]
        uc = UserProfileWriteableUseCaseImpl(uow)

        result = uc.get_or_create_settings(USER_ID)

        uow.settings_repository.create.assert_called_once()
        assert result.user_id == USER_ID

    def test_update_settings_changes_language(self):
        existing = _make_settings()
        uow = _make_uow(settings=existing)
        uc = UserProfileWriteableUseCaseImpl(uow)
        req = UpdateSettingsRequest(language=Language.ID)

        result = uc.update_settings(USER_ID, req)

        uow.settings_repository.update.assert_called_once()
        assert result.language == Language.ID

    def test_update_settings_validates_timezone(self):
        with pytest.raises(Exception):
            UpdateSettingsRequest(timezone="Invalid/Zone")

    def test_rollback_called_on_create_failure(self):
        uow = _make_uow(profile=None)
        uow.profile_repository.find_by_user_id.return_value = None
        uow.profile_repository.create.side_effect = RuntimeError("db error")
        uc = UserProfileWriteableUseCaseImpl(uow)

        with pytest.raises(RuntimeError):
            uc.get_or_create_profile(USER_ID)

        uow.rollback.assert_called_once()
