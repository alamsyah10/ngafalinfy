from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    email: str
    display_name: str | None
    provider: str | None  # e.g., "google", "local"

    provider_sub: str | None = None
    picture_url: str | None = None
    password_hash: str | None = None
    id: int | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now, compare=False)
    updated_at: datetime = field(default_factory=datetime.now, compare=False)

    def get_id(self) -> int | None:
        return self.id

    def update(
        self,
        display_name: str | None = None,
        picture_url: str | None = None,
        is_active: bool | None = None,
        provider: str | None = None,
        provider_sub: str | None = None,
    ) -> "User":
        return User(
            email=self.email,
            display_name=display_name
            if display_name is not None
            else self.display_name,
            provider=provider if provider is not None else self.provider,
            provider_sub=provider_sub
            if provider_sub is not None
            else self.provider_sub,
            picture_url=picture_url if picture_url is not None else self.picture_url,
            password_hash=self.password_hash,
            id=self.id,
            is_active=is_active if is_active is not None else self.is_active,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    @classmethod
    def new_google_user(
        cls,
        email: str,
        display_name: str | None,
        provider_sub: str,
        picture_url: str | None = None,
    ) -> "User":
        return cls(
            email=email,
            display_name=display_name,
            provider="google",
            provider_sub=provider_sub,
            picture_url=picture_url,
            password_hash=None,
            is_active=True,
        )

    @classmethod
    def new_local_user(
        cls,
        email: str,
        display_name: str,
        password_hash: str,
    ) -> "User":
        return cls(
            email=email,
            display_name=display_name,
            provider="local",
            provider_sub=None,
            picture_url=None,
            password_hash=password_hash,
            is_active=True,
        )
