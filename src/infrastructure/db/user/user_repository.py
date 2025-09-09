from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.domain.model.user.user import User
from src.domain.repository.user import UserRepository
from src.infrastructure.db.user.user_dto import UserDTO


class UserRepositoryImpl(UserRepository):
    """
    UserRepositoryImpl implements CRUD operations related User entity.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        try:
            user_dto = self.session.query(UserDTO).filter_by(email=email).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_entity()

    def create(self, user: User) -> User:
        user_dto = UserDTO.from_entity(user)

        try:
            self.session.add(user_dto)
        except:
            raise

        self.session.flush()
        return user_dto.to_entity()

    def upsert_google_identity(
        self, *, email: str, name: str | None, sub: str, picture: str | None
    ) -> User:
        user = self.get_by_email(email)
        if user is None:
            user = User.new_google_user(
                email=email, display_name=name, provider_sub=sub, picture_url=picture
            )
            return self.create(user)

        if user.provider is None:
            user = user.update(provider="google")
        if user.provider_sub is None:
            user = user.update(provider_sub=sub)
        if picture and user.picture_url != picture:
            user = user.update(picture_url=picture)

        self.session.flush()
        return user
