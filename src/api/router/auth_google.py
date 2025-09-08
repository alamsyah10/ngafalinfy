from fastapi import APIRouter, Depends, Request, status

from src.api.composition.auth_google import (
    google_callback_usecase,
    google_login_usecase,
    google_logout_usecase,
)
from src.api.error_schema.common import (
    ErrorMessageAuthorizationError,
    ErrorMessageInternalServerError,
    ErrorMessageOAuthAccountConflict,
    ErrorMessageOAuthAuthenticationFailed,
    ErrorMessageOAuthInvalidUserInfo,
)
from src.usecase.user.user_schema import (
    AuthTokenResponse,
)
from src.usecase.user.user_writeable_usecase import UserWriteableUsecase

router = APIRouter(prefix="/auth/google", tags=["auth:google"])


@router.get(
    "/login",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "OAuth client not configured",
        }
    },
    operation_id="google_login",
    summary="Start Google OAuth login",
)
async def google_login(
    request: Request,
    usecase: UserWriteableUsecase = Depends(google_login_usecase),
):
    return await usecase.login_redirect(request)


@router.get(
    "/callback",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorMessageOAuthInvalidUserInfo,
            "description": "Invalid user info from Google",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageOAuthAccountConflict,
            "description": "Account conflict (email already exists)",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageOAuthAuthenticationFailed,
            "description": "Authentication failed",
        },
    },
    operation_id="google_callback",
    summary="Handle Google OAuth callback",
)
async def google_callback(
    request: Request,
    usecase: UserWriteableUsecase = Depends(google_callback_usecase),
):
    return await usecase.oauth_callback(request)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "No active session",
        },
    },
    operation_id="google_logout",
    summary="Log out",
)
async def google_logout(
    request: Request,
    usecase: UserWriteableUsecase = Depends(google_logout_usecase),
):
    return usecase.logout(request)
