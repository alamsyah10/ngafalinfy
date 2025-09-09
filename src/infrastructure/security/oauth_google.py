from collections.abc import Callable
from typing import cast

from authlib.integrations.starlette_client import OAuth

from src.config import settings
from src.usecase.user.user_writeable_usecase import OAuthClientProto


def get_oauth() -> OAuth:
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    return oauth


def get_oauth_client_factory(oauth: OAuth) -> Callable[[str], OAuthClientProto | None]:
    def factory(name: str) -> OAuthClientProto | None:
        if name != "google":
            return None
        return cast(OAuthClientProto | None, oauth.create_client(name))

    return factory
