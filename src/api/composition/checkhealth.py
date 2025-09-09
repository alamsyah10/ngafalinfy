from src.config import settings
from src.domain.model.health import HealthCheckResponse, TestAccessResponse


def health_check_usecase() -> HealthCheckResponse:
    return HealthCheckResponse(
        name=settings.API_NAME,
        version=settings.VERSION,
    )


def test_access_usecase(user_id: int) -> TestAccessResponse:
    return TestAccessResponse(ok=True, user_id=user_id)
