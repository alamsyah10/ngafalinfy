from fastapi import Request

from src.domain.error.base import UnauthorizedError
from src.domain.ports.token import TokenDecoder


class AuthUsecase:
    def __init__(self, decoder: TokenDecoder, cookie_name: str):
        self.decoder = decoder
        self.cookie_name = cookie_name

    def extract_token(self, request: Request, authorization: str | None) -> str:
        if authorization and authorization.lower().startswith("bearer "):
            return authorization.split(" ", 1)[1].strip()

        token = request.cookies.get(self.cookie_name)
        if token:
            return token

        raise UnauthorizedError("Not authenticated")

    def get_current_user_id(self, token: str) -> int:
        try:
            payload = self.decoder.decode(token)
            sub = payload.get("sub")
            if not sub:
                raise UnauthorizedError("Invalid token: missing subject")
            return int(sub)
        except Exception:
            raise UnauthorizedError("Invalid token")
