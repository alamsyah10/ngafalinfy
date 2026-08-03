from datetime import datetime

from pydantic import Field, field_validator

from src.domain.model.common import CustomBaseModel
from src.domain.model.user.user_settings import (
    VALID_TIMEZONES,
    Language,
    ThemePreference,
)


class UserProfileResponse(CustomBaseModel):
    id: int
    user_id: int
    bio: str | None
    avatar_url: str | None
    phone: str | None
    location: str | None
    website: str | None
    created_at: datetime
    updated_at: datetime


class UpdateProfileRequest(CustomBaseModel):
    bio: str | None = Field(default=None, max_length=500)
    avatar_url: str | None = Field(default=None, max_length=512)
    phone: str | None = Field(default=None, max_length=20)
    location: str | None = Field(default=None, max_length=100)
    website: str | None = Field(default=None, max_length=255)


class UserSettingsResponse(CustomBaseModel):
    id: int
    user_id: int
    language: Language
    timezone: str
    theme: ThemePreference
    daily_review_goal: int
    notifications_enabled: bool
    created_at: datetime
    updated_at: datetime


class UpdateSettingsRequest(CustomBaseModel):
    language: Language | None = None
    timezone: str | None = Field(default=None, max_length=50)
    theme: ThemePreference | None = None
    daily_review_goal: int | None = Field(default=None, ge=1, le=500)
    notifications_enabled: bool | None = None

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v: str | None) -> str | None:
        if v is not None and v not in VALID_TIMEZONES:
            raise ValueError(f"unsupported timezone: {v!r}")
        return v
