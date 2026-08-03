from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.db.core import get_session
from src.infrastructure.db.user.user_profile_query_service import (
    UserProfileReadableServiceImpl,
)
from src.infrastructure.db.user.user_profile_repository import UserProfileRepositoryImpl
from src.infrastructure.db.user.user_profile_repository_usecase import (
    UserProfileRepositoryUseCaseUnitOfWorkImpl,
)
from src.infrastructure.db.user.user_settings_repository import (
    UserSettingsRepositoryImpl,
)
from src.usecase.user.user_profile_readable_service import UserProfileReadableService
from src.usecase.user.user_profile_readable_usecase import (
    UserProfileReadableUseCase,
    UserProfileReadableUseCaseImpl,
)
from src.usecase.user.user_profile_writeable_usecase import (
    UserProfileWriteableUseCase,
    UserProfileWriteableUseCaseImpl,
    UserProfileWriteableUseCaseUnitOfWork,
)


def user_profile_read_usecase(
    session: Session = Depends(get_session),
) -> UserProfileReadableUseCase:
    service: UserProfileReadableService = UserProfileReadableServiceImpl(session)
    return UserProfileReadableUseCaseImpl(service)


def user_profile_write_usecase(
    session: Session = Depends(get_session),
) -> UserProfileWriteableUseCase:
    profile_repo = UserProfileRepositoryImpl(session)
    settings_repo = UserSettingsRepositoryImpl(session)
    uow: UserProfileWriteableUseCaseUnitOfWork = (
        UserProfileRepositoryUseCaseUnitOfWorkImpl(
            session=session,
            profile_repository=profile_repo,
            settings_repository=settings_repo,
        )
    )
    return UserProfileWriteableUseCaseImpl(uow)
