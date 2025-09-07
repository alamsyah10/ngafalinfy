from typing import Any, Protocol


class TokenDecoder(Protocol):
    def decode(self, token: str) -> dict[str, Any]: ...
