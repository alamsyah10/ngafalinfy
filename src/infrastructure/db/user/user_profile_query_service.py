from sqlalchemy.orm import Session

from src.infrastructure.db.user.user_profile_dto import UserProfileDTO
from src.infrastructure.db.user.user_settings_dto import UserSettingsDTO
from src.usecase.user.user_profile_readable_service import UserProfileReadableService
from src.usecase.user.user_profile_schema import (
    UserProfileResponse,
    UserSettingsResponse,
)


class UserProfileReadableServiceImpl(UserProfileReadableService):
    def __init__(self, session: Session):
        self.session = session

    def find_profile_by_user_id(self, user_id: int) -> UserProfileResponse | None:
        dto = (
            self.session.query(UserProfileDTO).filter_by(user_id=user_id).one_or_none()
        )
        return dto.to_response_model() if dto else None

    def find_settings_by_user_id(self, user_id: int) -> UserSettingsResponse | None:
        dto = (
            self.session.query(UserSettingsDTO).filter_by(user_id=user_id).one_or_none()
        )
        return dto.to_response_model() if dto else None
