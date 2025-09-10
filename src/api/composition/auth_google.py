from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.db.core import get_session
from src.infrastructure.db.user.user_repository import UserRepositoryImpl
from src.infrastructure.db.user.user_repository_usecase import (
    UserWriteableUseCaseUnitOfWorkImpl,
)
from src.infrastructure.security.oauth_google import get_oauth, get_oauth_client_factory
from src.usecase.user.user_writeable_usecase import (
    UserWriteableUsecase,
    UserWriteableUsecaseImpl,
)


def _provide_usecase(
    db: Session = Depends(get_session),
    oauth=Depends(get_oauth),
) -> UserWriteableUsecase:
    uow = UserWriteableUseCaseUnitOfWorkImpl(
        session=db,
        user_repository=UserRepositoryImpl(db),
        oauth_client_factory=get_oauth_client_factory(oauth),
    )
    return UserWriteableUsecaseImpl(uow)


def google_login_usecase(
    usecase: UserWriteableUsecase = Depends(_provide_usecase),
) -> UserWriteableUsecase:
    return usecase


def google_callback_usecase(
    usecase: UserWriteableUsecase = Depends(_provide_usecase),
) -> UserWriteableUsecase:
    return usecase


def google_logout_usecase(
    usecase: UserWriteableUsecase = Depends(_provide_usecase),
) -> UserWriteableUsecase:
    return usecase
