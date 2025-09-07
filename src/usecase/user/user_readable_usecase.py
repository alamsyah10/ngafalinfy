from sqlalchemy.orm import Session

from src.domain.error.base import InternalServerError, UserNotFoundError
from src.domain.repository.user import UserRepository
from src.infrastructure.db.user.user_dto import UserDTO


class UserReadableUsecase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_me(self, db: Session, user_id: int) -> UserDTO:
        try:
            user = db.get(self.repo.entity_cls, user_id)
        except Exception:
            raise InternalServerError("Database unavailable")

        if not user:
            raise UserNotFoundError(f"User with id={user_id} not found")

        return UserDTO.from_entity(user)
