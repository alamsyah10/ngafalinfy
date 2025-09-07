from sqlalchemy.orm import Session

from src.config import settings
from src.domain.error.base import InternalServerError
from src.domain.model.health import HealthCheckResponse, MeResponse, TestAccessResponse
from src.infrastructure.db.user.user_repository import UserRepositoryImpl
from src.usecase.user.user_readable_usecase import UserReadableUsecase


def health_check_usecase() -> HealthCheckResponse:
    return HealthCheckResponse(
        name=settings.API_NAME,
        version=settings.VERSION,
    )


def test_access_usecase(user_id: int) -> TestAccessResponse:
    return TestAccessResponse(ok=True, user_id=user_id)


def me_usecase(db: Session, user_id: int) -> MeResponse:
    try:
        repo = UserRepositoryImpl(db)
        uc = UserReadableUsecase(repo)
        dto = uc.get_me(db, user_id)
    except Exception as e:
        raise InternalServerError(str(e))

    return MeResponse(
        id=dto.id,
        email=dto.email,
        display_name=dto.display_name,
        picture_url=dto.picture_url,
        provider=dto.provider,
    )
