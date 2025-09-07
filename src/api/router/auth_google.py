from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

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
from src.domain.model.auth import AuthTokenResponse
from src.infrastructure.db.core import get_session

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
    summary="Start Google OAuth login",
    description="Redirects the user to Google for authentication.",
)
async def google_login(request: Request):
    return await google_login_usecase(request)


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
    summary="Handle Google OAuth callback",
    description="Exchanges the Google OAuth code for a token and logs in the user.",
)
async def google_callback(request: Request, db: Session = Depends(get_session)):
    return await google_callback_usecase(request, db)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "No active session",
        },
    },
    summary="Log out",
    description="Clears the authentication cookie and ends the session.",
)
async def google_logout(request: Request):
    return google_logout_usecase(request)
