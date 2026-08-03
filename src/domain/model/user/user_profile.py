from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class UserProfile:
    user_id: int
    bio: str | None = None
    avatar_url: str | None = None
    phone: str | None = None
    location: str | None = None
    website: str | None = None
    id: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def get_id(self) -> int | None:
        return self.id

    def update(
        self,
        bio: str | None = None,
        avatar_url: str | None = None,
        phone: str | None = None,
        location: str | None = None,
        website: str | None = None,
    ) -> "UserProfile":
        return UserProfile(
            id=self.id,
            user_id=self.user_id,
            bio=bio if bio is not None else self.bio,
            avatar_url=avatar_url if avatar_url is not None else self.avatar_url,
            phone=phone if phone is not None else self.phone,
            location=location if location is not None else self.location,
            website=website if website is not None else self.website,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
        )

    @classmethod
    def default_for(cls, user_id: int) -> "UserProfile":
        """Create a default empty profile for a new user."""
        return cls(user_id=user_id)
