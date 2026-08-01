from abc import ABC, abstractmethod

from fastapi_pagination import Page, Params

from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse


class ReviewLogReadableService(ABC):
    """
    ReviewLogReadableService defines a query service interface related to ReviewLog entity
    Review logs are immutable history records of user reviews
    """

    @abstractmethod
    def list_all_by_card_id(
        self,
        card_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        """
        Paginated review history for a specific card
        """
        raise NotImplementedError

    @abstractmethod
    def list_all_by_deck_id(
        self,
        deck_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        """
        Paginated review logs across all cards in a deck
        (Usually implemented by joining review_logs -> cards on card_id)
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> ReviewLogDigestResponse | None:
        """
        Find a review log by its id
        """
        raise NotImplementedError

    @abstractmethod
    def get_latest_by_card_id(self, card_id: int) -> ReviewLogDigestResponse | None:
        """
        Get the latest review log for a card
        """
        raise NotImplementedError

    @abstractmethod
    def count_by_card_id(self, card_id: int) -> int:
        """
        Count review logs for a card
        """
        raise NotImplementedError

    @abstractmethod
    def count_by_deck_id(self, deck_id: int) -> int:
        """
        Count review logs across all cards in a deck
        """
        raise NotImplementedError
