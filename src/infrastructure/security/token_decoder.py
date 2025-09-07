from typing import Any

from jose import jwt

from src.config import settings
from src.domain.ports.token import TokenDecoder


class JoseTokenDecoder(TokenDecoder):
    def decode(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALG])
