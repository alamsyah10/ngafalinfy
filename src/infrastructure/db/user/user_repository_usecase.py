from collections.abc import Callable

from sqlalchemy.orm import Session

from src.domain.model.user.user import User
from src.domain.repository.user import UserRepository
from src.usecase.user.user_writeable_usecase import (
    OAuthClientProto,
    UserWriteableUseCaseUnitOfWork,
)


class UserWriteableUseCaseUnitOfWorkImpl(UserWriteableUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
        oauth_client_factory: Callable[[str], OAuthClientProto | None],
    ):
        self.session: Session = session
        self.user_repository: UserRepository = user_repository
        self.oauth_client_factory: Callable[[str], OAuthClientProto | None] = (
            oauth_client_factory
        )

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def refresh(self, user: User):
        self.session.refresh(user)
