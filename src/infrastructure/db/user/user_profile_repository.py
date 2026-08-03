from sqlalchemy.orm import Session

from src.domain.model.user.user_profile import UserProfile
from src.domain.repository.user_profile import UserProfileRepository
from src.infrastructure.db.user.user_profile_dto import UserProfileDTO


class UserProfileRepositoryImpl(UserProfileRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_user_id(self, user_id: int) -> UserProfile | None:
        dto = (
            self.session.query(UserProfileDTO).filter_by(user_id=user_id).one_or_none()
        )
        return dto.to_entity() if dto else None

    def create(self, profile: UserProfile) -> None:
        dto = UserProfileDTO.from_entity(profile)
        self.session.add(dto)

    def update(self, profile: UserProfile) -> None:
        row = (
            self.session.query(UserProfileDTO).filter_by(user_id=profile.user_id).one()
        )
        row.bio = profile.bio
        row.avatar_url = profile.avatar_url
        row.phone = profile.phone
        row.location = profile.location
        row.website = profile.website
        row.updated_at = profile.updated_at
