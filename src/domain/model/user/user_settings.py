from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class Language(StrEnum):
    EN = "en"
    ID = "id"


class ThemePreference(StrEnum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


VALID_TIMEZONES: frozenset[str] = frozenset(
    [
        "UTC",
        "Asia/Jakarta",
        "Asia/Makassar",
        "Asia/Jayapura",
        "Asia/Singapore",
        "Asia/Tokyo",
        "Asia/Bangkok",
        "Asia/Kolkata",
        "Europe/London",
        "Europe/Paris",
        "America/New_York",
        "America/Los_Angeles",
        "America/Chicago",
        "Australia/Sydney",
    ]
)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserSettings:
    user_id: int
    language: Language = Language.EN
    timezone: str = "UTC"
    theme: ThemePreference = ThemePreference.SYSTEM
    daily_review_goal: int = 20
    notifications_enabled: bool = True
    id: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def get_id(self) -> int | None:
        return self.id

    def update(
        self,
        language: Language | None = None,
        timezone: str | None = None,
        theme: ThemePreference | None = None,
        daily_review_goal: int | None = None,
        notifications_enabled: bool | None = None,
    ) -> "UserSettings":
        return UserSettings(
            id=self.id,
            user_id=self.user_id,
            language=language if language is not None else self.language,
            timezone=timezone if timezone is not None else self.timezone,
            theme=theme if theme is not None else self.theme,
            daily_review_goal=daily_review_goal
            if daily_review_goal is not None
            else self.daily_review_goal,
            notifications_enabled=notifications_enabled
            if notifications_enabled is not None
            else self.notifications_enabled,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
        )

    @classmethod
    def default_for(cls, user_id: int) -> "UserSettings":
        """Create default settings for a new user."""
        return cls(user_id=user_id)
