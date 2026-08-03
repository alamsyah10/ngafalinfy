from sqlalchemy.orm import Session

from src.domain.model.user.user_settings import UserSettings
from src.domain.repository.user_settings import UserSettingsRepository
from src.infrastructure.db.user.user_settings_dto import UserSettingsDTO


class UserSettingsRepositoryImpl(UserSettingsRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_user_id(self, user_id: int) -> UserSettings | None:
        dto = (
            self.session.query(UserSettingsDTO).filter_by(user_id=user_id).one_or_none()
        )
        return dto.to_entity() if dto else None

    def create(self, settings: UserSettings) -> None:
        dto = UserSettingsDTO.from_entity(settings)
        self.session.add(dto)

    def update(self, settings: UserSettings) -> None:
        row = (
            self.session.query(UserSettingsDTO)
            .filter_by(user_id=settings.user_id)
            .one()
        )
        row.language = settings.language.value
        row.timezone = settings.timezone
        row.theme = settings.theme.value
        row.daily_review_goal = settings.daily_review_goal
        row.notifications_enabled = settings.notifications_enabled
        row.updated_at = settings.updated_at
