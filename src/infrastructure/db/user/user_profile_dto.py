from src.domain.model.user.user_profile import UserProfile
from src.infrastructure.db.user.user_profile_table import UserProfileTable
from src.usecase.user.user_profile_schema import UserProfileResponse


class UserProfileDTO(UserProfileTable):
    def to_entity(self) -> UserProfile:
        return UserProfile(
            id=self.id,
            user_id=self.user_id,
            bio=self.bio,
            avatar_url=self.avatar_url,
            phone=self.phone,
            location=self.location,
            website=self.website,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_response_model(self) -> UserProfileResponse:
        return UserProfileResponse(
            id=self.id,
            user_id=self.user_id,
            bio=self.bio,
            avatar_url=self.avatar_url,
            phone=self.phone,
            location=self.location,
            website=self.website,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, profile: UserProfile) -> "UserProfileDTO":
        return cls(
            id=profile.id,
            user_id=profile.user_id,
            bio=profile.bio,
            avatar_url=profile.avatar_url,
            phone=profile.phone,
            location=profile.location,
            website=profile.website,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )
