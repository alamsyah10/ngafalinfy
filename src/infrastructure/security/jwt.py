from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from src.config import settings


def create_access_token(claims: dict[str, Any]) -> str:
    now = datetime.now()
    payload = {
        **claims,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.JWT_EXPIRES_MIN)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALG)
