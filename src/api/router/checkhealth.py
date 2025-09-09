from fastapi import APIRouter, Depends, status

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.checkhealth import (
    health_check_usecase,
    test_access_usecase,
)
from src.api.composition.user import user_read_usecase
from src.api.error_schema.common import (
    ErrorMessageAuthorizationError,
    ErrorMessageInternalServerError,
    ErrorMessageUserNotFoundError,
)
from src.domain.model.health import HealthCheckResponse, TestAccessResponse
from src.usecase.user.user_readable_usecase import UserReadableUseCase
from src.usecase.user.user_schema import AuthUserResponse

router = APIRouter(prefix="/checkhealth", tags=["checkhealth"])


@router.get(
    "",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    operation_id="health_check",
    summary="Health Check",
    description="Ngafalinfy API Health Check",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "Internal Server Error",
        }
    },
)
async def check_health() -> HealthCheckResponse:
    return health_check_usecase()


@router.get(
    "/test-access",
    response_model=TestAccessResponse,
    status_code=status.HTTP_200_OK,
    operation_id="test_access",
    summary="Access Test",
    description="JWT access test (requires valid token)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "Unauthorized",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "Internal Server Error",
        },
    },
)
def test_access(
    user_id: int = Depends(get_current_user_id_usecase),
) -> TestAccessResponse:
    return test_access_usecase(user_id)


@router.get(
    "/me",
    response_model=AuthUserResponse,
    status_code=status.HTTP_200_OK,
    operation_id="who_am_i",
    summary="Current User Info",
    description="Returns the current user's basic profile from the DB",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFoundError,
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "Internal Server Error",
        },
    },
)
def me(
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: UserReadableUseCase = Depends(user_read_usecase),
) -> AuthUserResponse:
    return usecase.fetch_user(user_id)
