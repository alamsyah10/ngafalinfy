from abc import ABC, abstractmethod

from src.domain.model.review_log.review_log import ReviewLog


class ReviewLogRepository(ABC):
    """
    ReviewLogRepository defines a repository interface for ReviewLog entity.
    ReviewLog is an immutable audit/history record of a review action
    """

    @abstractmethod
    def create_log(self, log: ReviewLog) -> ReviewLog:
        """
        Persist a review log record and return the created object
        (optionally with generated id / timestamps)
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> ReviewLog | None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        """
        Normally you might never delete logs, but keeping it for admin/test cleanup
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_card_id(
        self,
        card_id: int,
        limit: int | None = None,
        newest_first: bool = True,
    ) -> list[ReviewLog]:
        """
        Get review history for a card
        """
        raise NotImplementedError

    @abstractmethod
    def get_latest_by_card_id(self, card_id: int) -> ReviewLog | None:
        """
        Get the latest review log for a card (if any)
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_deck_id(
        self,
        deck_id: int,
        limit: int | None = None,
        newest_first: bool = True,
    ) -> list[ReviewLog]:
        """
        Convenience: get logs for all cards in a deck.
        Implementation usually joins review_logs -> cards on card_id
        """
        raise NotImplementedError

    @abstractmethod
    def delete_by_card_id(self, card_id: int) -> None:
        """
        When a card is deleted, logs might be cascade-deleted by FK,
        but this method is useful for explicit cleanup in some cases/tests
        """
        raise NotImplementedError
