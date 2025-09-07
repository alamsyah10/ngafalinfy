import logging
from collections.abc import Callable
from typing import Protocol, runtime_checkable

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config import settings
from src.domain.error.base import (
    InternalServerError,
    OAuthAuthenticationFailedError,
    OAuthClientNotConfiguredError,
    OAuthInvalidUserInfoError,
    ResourceConflictError,
    UnauthorizedError,
)
from src.domain.repository.user import UserRepository
from src.infrastructure.db.user.user_dto import UserDTO
from src.infrastructure.security.jwt import create_access_token

logger = logging.getLogger("backend")


@runtime_checkable
class OAuthClientProto(Protocol):
    async def authorize_redirect(self, request: Request, redirect_uri: str): ...
    async def authorize_access_token(self, request: Request) -> dict: ...
    async def userinfo(self, *, token: dict) -> dict: ...
    async def parse_id_token(self, request: Request, token: dict) -> dict: ...


class UserWriteableUsecase:
    def __init__(
        self,
        oauth_client_factory: Callable[[str], OAuthClientProto | None],
        repo: UserRepository | None = None,
    ):
        self.repo = repo
        self.oauth_client_factory = oauth_client_factory

    async def login_redirect(self, request: Request):
        client = self.oauth_client_factory("google")
        if client is None:
            raise OAuthClientNotConfiguredError()
        try:
            return await client.authorize_redirect(
                request, settings.GOOGLE_REDIRECT_URI
            )
        except Exception as e:
            logger.exception("authorize_redirect failed: %s", e)
            raise OAuthAuthenticationFailedError()

    async def oauth_callback(self, request: Request, db: Session) -> JSONResponse:
        if self.repo is None:
            raise InternalServerError("User repository not provided")

        client = self.oauth_client_factory("google")
        if client is None:
            raise OAuthClientNotConfiguredError()

        try:
            token = await client.authorize_access_token(request)
            logger.debug({"oauth_token_keys": list(token.keys())})

            try:
                userinfo: dict | None = await client.userinfo(token=token)
            except Exception as e:
                logger.warning("userinfo() failed, fallback to parse_id_token: %s", e)
                id_token = await client.parse_id_token(request, token)
                userinfo = {
                    "sub": id_token.get("sub"),
                    "email": id_token.get("email"),
                    "name": id_token.get("name") or id_token.get("given_name"),
                    "picture": id_token.get("picture"),
                }

            if not userinfo or not userinfo.get("email") or not userinfo.get("sub"):
                logger.error("Invalid user info: %s", userinfo)
                raise OAuthInvalidUserInfoError("Google userinfo missing email or sub")

            email = userinfo["email"]
            sub = userinfo["sub"]
            name = userinfo.get("name")
            picture = userinfo.get("picture")

            user = self.repo.upsert_google_identity(  # type: ignore[union-attr]  (repo is not None here)
                email=email, name=name, sub=sub, picture=picture
            )

            try:
                db.commit()
            except IntegrityError as ie:
                db.rollback()
                logger.exception("DB integrity error on user upsert: %s", ie)
                raise ResourceConflictError("Account already exists")

            db.refresh(user)

            dto = UserDTO.from_entity(user)
            access = create_access_token(
                {"sub": str(dto.id), "email": dto.email, "name": dto.display_name or ""}
            )

            resp = JSONResponse(
                {
                    "access_token": access,
                    "token_type": "bearer",
                    "user": dto.to_auth_user().model_dump(),
                }
            )
            resp.set_cookie(
                key=settings.COOKIE_NAME,
                value=access,
                httponly=True,
                secure=settings.SESSION_HTTPS_ONLY,
                samesite=settings.SESSION_SAMESITE,
                max_age=settings.JWT_EXPIRES_MIN * 60,
                path="/",
            )
            return resp

        except (
            OAuthClientNotConfiguredError,
            OAuthInvalidUserInfoError,
            ResourceConflictError,
        ):
            raise
        except Exception as e:
            logger.exception("Google callback failed: %s", e)
            raise OAuthAuthenticationFailedError()

    def logout(self, request: Request) -> JSONResponse:
        token = request.cookies.get(settings.COOKIE_NAME)
        if not token:
            raise UnauthorizedError("No active session")

        resp = JSONResponse({"message": "Signed out successfully"})
        resp.delete_cookie(key=settings.COOKIE_NAME, path="/")
        return resp
