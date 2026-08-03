from sqlalchemy.orm import Session

from src.domain.repository.user_profile import UserProfileRepository
from src.domain.repository.user_settings import UserSettingsRepository
from src.usecase.user.user_profile_writeable_usecase import (
    UserProfileWriteableUseCaseUnitOfWork,
)


class UserProfileRepositoryUseCaseUnitOfWorkImpl(UserProfileWriteableUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        profile_repository: UserProfileRepository,
        settings_repository: UserSettingsRepository,
    ):
        self.session = session
        self.profile_repository = profile_repository
        self.settings_repository = settings_repository

    def begin(self) -> None:
        self.session.begin()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
