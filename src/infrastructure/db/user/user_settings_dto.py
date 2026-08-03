from src.domain.model.user.user_settings import Language, ThemePreference, UserSettings
from src.infrastructure.db.user.user_settings_table import UserSettingsTable
from src.usecase.user.user_profile_schema import UserSettingsResponse


class UserSettingsDTO(UserSettingsTable):
    def to_entity(self) -> UserSettings:
        return UserSettings(
            id=self.id,
            user_id=self.user_id,
            language=Language(self.language),
            timezone=self.timezone,
            theme=ThemePreference(self.theme),
            daily_review_goal=self.daily_review_goal,
            notifications_enabled=self.notifications_enabled,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_response_model(self) -> UserSettingsResponse:
        return UserSettingsResponse(
            id=self.id,
            user_id=self.user_id,
            language=Language(self.language),
            timezone=self.timezone,
            theme=ThemePreference(self.theme),
            daily_review_goal=self.daily_review_goal,
            notifications_enabled=self.notifications_enabled,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, settings: UserSettings) -> "UserSettingsDTO":
        return cls(
            id=settings.id,
            user_id=settings.user_id,
            language=settings.language.value,
            timezone=settings.timezone,
            theme=settings.theme.value,
            daily_review_goal=settings.daily_review_goal,
            notifications_enabled=settings.notifications_enabled,
            created_at=settings.created_at,
            updated_at=settings.updated_at,
        )
