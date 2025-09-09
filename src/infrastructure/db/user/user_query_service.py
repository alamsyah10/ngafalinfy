from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.infrastructure.db.user.user_dto import UserDTO
from src.usecase.user.user_readable_service import UserReadableService
from src.usecase.user.user_schema import AuthUserResponse


class UserReadableServiceImpl(UserReadableService):
    """
    UserReadableServiceImpl implements READ operations related
    User entity using SQLAlchemy.
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, user_id: int) -> AuthUserResponse | None:
        try:
            user_dto = self.session.query(UserDTO).filter_by(id=user_id).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_auth_user()
