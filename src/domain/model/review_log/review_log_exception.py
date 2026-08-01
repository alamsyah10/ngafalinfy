from src.domain.error.base import ResourceNotFoundError


class ReviewLogNotFoundError(ResourceNotFoundError):
    def __init__(self, id: int):
        super().__init__(message=f"review_log[{id}] is not found")


class NoReviewLogsForCardError(ResourceNotFoundError):
    """
    Raised when a card exists but has no review logs yet.
    Useful when a caller expects at least one review history (e.g., latest log).
    """

    def __init__(self, card_id: int):
        super().__init__(message=f"card[{card_id}] has no review logs")
