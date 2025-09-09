from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.db.core import get_session
from src.infrastructure.db.user.user_query_service import UserReadableServiceImpl
from src.usecase.user.user_readable_usecase import (
    UserReadableService,
    UserReadableUseCase,
    UserReadableUseCaseImpl,
)


def user_read_usecase(
    session: Session = Depends(get_session),
) -> UserReadableUseCase:
    service: UserReadableService = UserReadableServiceImpl(session)
    return UserReadableUseCaseImpl(service)
