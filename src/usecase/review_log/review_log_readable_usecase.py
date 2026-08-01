from abc import ABC, abstractmethod

from fastapi_pagination import Page, Params

from src.domain.model.review_log.review_log_exception import (
    NoReviewLogsForCardError,
    ReviewLogNotFoundError,
)
from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse

from .review_log_readable_service import ReviewLogReadableService


class ReviewLogReadableUseCase(ABC):
    """
    ReviewLogReadableUseCase defines a query usecase interface related to ReviewLog entity
    """

    @abstractmethod
    def fetch_log_by_id(self, id: int) -> ReviewLogDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def fetch_logs_by_card_id(
        self,
        card_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        raise NotImplementedError

    @abstractmethod
    def fetch_logs_by_deck_id(
        self,
        deck_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        raise NotImplementedError

    @abstractmethod
    def fetch_latest_log_by_card_id(self, card_id: int) -> ReviewLogDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def fetch_log_count_by_card_id(self, card_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def fetch_log_count_by_deck_id(self, deck_id: int) -> int:
        raise NotImplementedError


class ReviewLogReadableUseCaseImpl(ReviewLogReadableUseCase):
    """
    ReviewLogReadableUseCaseImpl implements query usecases related to ReviewLog entity
    """

    def __init__(self, review_log_service: ReviewLogReadableService):
        self.review_log_service: ReviewLogReadableService = review_log_service

    def fetch_log_by_id(self, id: int) -> ReviewLogDigestResponse:
        log = self.review_log_service.find_by_id(id)
        if log is None:
            raise ReviewLogNotFoundError(id)
        return log

    def fetch_logs_by_card_id(
        self,
        card_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        return self.review_log_service.list_all_by_card_id(
            card_id=card_id,
            params=params,
            newest_first=newest_first,
        )

    def fetch_logs_by_deck_id(
        self,
        deck_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        return self.review_log_service.list_all_by_deck_id(
            deck_id=deck_id,
            params=params,
            newest_first=newest_first,
        )

    def fetch_latest_log_by_card_id(self, card_id: int) -> ReviewLogDigestResponse:
        log = self.review_log_service.get_latest_by_card_id(card_id)
        if log is None:
            raise NoReviewLogsForCardError(card_id)
        return log

    def fetch_log_count_by_card_id(self, card_id: int) -> int:
        return self.review_log_service.count_by_card_id(card_id)

    def fetch_log_count_by_deck_id(self, deck_id: int) -> int:
        return self.review_log_service.count_by_deck_id(deck_id)
