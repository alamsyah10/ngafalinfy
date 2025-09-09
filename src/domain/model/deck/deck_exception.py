from src.domain.error.base import ResourceNotFoundError


class DeckNotFoundError(ResourceNotFoundError):
    def __init__(self, id: int):
        message = f"deck[{id}] is not found"
        super().__init__(message=message)
