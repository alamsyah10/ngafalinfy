from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.infrastructure.db.user.user_repository import UserRepositoryImpl
from src.infrastructure.security.oauth_google import oauth
from src.usecase.user.user_writeable_usecase import UserWriteableUsecase


async def google_login_usecase(request: Request):
    uc = UserWriteableUsecase(oauth_client_factory=oauth.create_client)
    return await uc.login_redirect(request)


async def google_callback_usecase(request: Request, db: Session) -> JSONResponse:
    uc = UserWriteableUsecase(
        oauth_client_factory=oauth.create_client,
        repo=UserRepositoryImpl(db=db),
    )
    return await uc.oauth_callback(request, db)


def google_logout_usecase(request: Request) -> JSONResponse:
    uc = UserWriteableUsecase(oauth_client_factory=oauth.create_client)
    return uc.logout(request)
