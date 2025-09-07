from sqlalchemy.orm import Session

from src.domain.repository.user import UserRepository

from .user_table import User


class UserRepositoryImpl(UserRepository):
    entity_cls: type[User] = User

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(
        self,
        *,
        email: str,
        display_name: str | None,
        picture_url: str | None,
        provider: str | None,
        provider_sub: str | None,
        is_active: bool = True,
    ) -> User:
        user = User(
            email=email,
            display_name=display_name,
            picture_url=picture_url,
            provider=provider,
            provider_sub=provider_sub,
            is_active=is_active,
        )
        self.db.add(user)
        self.db.flush()
        return user

    def upsert_google_identity(
        self, *, email: str, name: str | None, sub: str, picture: str | None
    ) -> User:
        user = self.get_by_email(email)
        if user is None:
            return self.create(
                email=email,
                display_name=name,
                provider="google",
                provider_sub=sub,
                picture_url=picture,
                is_active=True,
            )

        if user.provider is None:
            user.provider = "google"
        if user.provider_sub is None:
            user.provider_sub = sub
        if picture and user.picture_url != picture:
            user.picture_url = picture

        self.db.flush()
        return user
