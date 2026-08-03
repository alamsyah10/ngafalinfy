from fastapi import APIRouter, Body, Depends, status

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.user_profile import (
    user_profile_write_usecase,
)
from src.api.error_schema.common import (
    ErrorMessageAuthorizationError,
    ErrorMessageInternalServerError,
    ErrorMessageValidationError,
)
from src.usecase.user.user_profile_schema import (
    UpdateProfileRequest,
    UserProfileResponse,
)
from src.usecase.user.user_profile_writeable_usecase import UserProfileWriteableUseCase

router = APIRouter(prefix="/me/profile", tags=["user-profile"])


@router.get(
    "",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_my_profile",
    summary="Get the current user's profile",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError
        },
    },
)
def get_my_profile(
    user_id: int = Depends(get_current_user_id_usecase),
    write_uc: UserProfileWriteableUseCase = Depends(user_profile_write_usecase),
) -> UserProfileResponse:
    # auto-create profile on first access
    return write_uc.get_or_create_profile(user_id)


@router.patch(
    "",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    operation_id="update_my_profile",
    summary="Update the current user's profile",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessageValidationError},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError
        },
    },
)
def update_my_profile(
    payload: UpdateProfileRequest = Body(...),
    user_id: int = Depends(get_current_user_id_usecase),
    write_uc: UserProfileWriteableUseCase = Depends(user_profile_write_usecase),
) -> UserProfileResponse:
    return write_uc.update_profile(user_id, payload)
