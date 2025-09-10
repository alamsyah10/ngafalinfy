from src.domain.error.base import ResourceNotFoundError


class CardNotFoundError(ResourceNotFoundError):
    def __init__(self, id: int):
        super().__init__(message=f"card[{id}] is not found")


class NoActiveCardsInDeckError(ResourceNotFoundError):
    """
    Raised when a deck exists but has no active cards to study.
    """

    def __init__(self, deck_id: int):
        super().__init__(message=f"deck[{deck_id}] has no active cards")
