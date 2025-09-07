from fastapi import Depends, Header, Request

from src.config import settings
from src.infrastructure.security.token_decoder import JoseTokenDecoder
from src.usecase.auth.auth_usecase import AuthUsecase


def _auth_uc() -> AuthUsecase:
    return AuthUsecase(decoder=JoseTokenDecoder(), cookie_name=settings.COOKIE_NAME)


def extract_token_usecase(
    request: Request,
    authorization: str | None = Header(None),
) -> str:
    return _auth_uc().extract_token(request, authorization)


def get_current_user_id_usecase(
    token: str = Depends(extract_token_usecase),
) -> int:
    return _auth_uc().get_current_user_id(token)
