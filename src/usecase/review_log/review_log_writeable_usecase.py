import logging
from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.model.card.card_exception import CardNotFoundError
from src.domain.model.deck.deck_exception import DeckNotFoundError
from src.domain.model.review_log.review_log import ReviewLog
from src.domain.model.review_log.review_log_exception import ReviewLogNotFoundError
from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.domain.repository.review_log import ReviewLogRepository
from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse

logger = logging.getLogger("backend")


class ReviewLogWriteableUseCaseUnitOfWork(ABC):
    """
    ReviewLogWritableUseCaseUnitOfWork defines an interface based on Unit of Work pattern.
    """

    deck_repository: DeckRepository
    card_repository: CardRepository
    review_log_repository: ReviewLogRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class ReviewLogWriteableUseCase(ABC):
    """
    ReviewLogWritableUseCase defines command usecases related to ReviewLog entity.

    Notes:
    - In most flashcard apps, review logs are append-only (immutable).
    - This usecase provides admin/test/maintenance actions for logs.
    """

    @abstractmethod
    def create_log(
        self,
        deck_id: int,
        card_id: int,
        owner_id: int,
        *,
        ease_given: int,
        prev_interval: int,
        new_interval: int,
        prev_ease: float,
        new_ease: float,
        reviewed_at: datetime | None = None,
    ) -> ReviewLogDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_log(self, id: int, deck_id: int, owner_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_logs_by_card_id(
        self, card_id: int, deck_id: int, owner_id: int
    ) -> None:
        raise NotImplementedError


class ReviewLogWriteableUseCaseImpl(ReviewLogWriteableUseCase):
    """
    ReviewLogWritableUseCaseImpl implements command usecases related to ReviewLog entity.
    """

    def __init__(self, uow: ReviewLogWriteableUseCaseUnitOfWork):
        self.uow = uow

    def _ensure_deck_owned(self, deck_id: int, owner_id: int):
        deck = self.uow.deck_repository.find_by_id_and_owner_id(deck_id, owner_id)
        if deck is None:
            raise DeckNotFoundError(deck_id)

    def _ensure_card_in_deck(self, card_id: int, deck_id: int):
        card = self.uow.card_repository.find_by_id_and_deck_id(card_id, deck_id)
        if card is None:
            raise CardNotFoundError(card_id)

    def create_log(
        self,
        deck_id: int,
        card_id: int,
        owner_id: int,
        *,
        ease_given: int,
        prev_interval: int,
        new_interval: int,
        prev_ease: float,
        new_ease: float,
        reviewed_at: datetime | None = None,
    ) -> ReviewLogDigestResponse:
        """
        Create a review log record.

        In a typical implementation, this is called by the "review card" usecase
        (which also updates Card scheduling fields) within the same transaction.
        """
        try:
            self.uow.begin()  # Explicitly start transaction
            self._ensure_deck_owned(deck_id, owner_id)
            self._ensure_card_in_deck(card_id, deck_id)

            log = ReviewLog.new(
                card_id=card_id,
                user_id=owner_id,
                ease_given=ease_given,
                prev_interval=prev_interval,
                new_interval=new_interval,
                prev_ease=prev_ease,
                new_ease=new_ease,
                reviewed_at=reviewed_at,
            )

            self.uow.review_log_repository.create_log(log)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise

        return ReviewLogDigestResponse.from_entity(log)

    def delete_log(self, id: int, deck_id: int, owner_id: int) -> None:
        """
        Delete a specific review log.
        (Usually admin/test-only; most apps keep review logs immutable.)
        """
        try:
            self.uow.begin()  # Explicitly start transaction
            self._ensure_deck_owned(deck_id, owner_id)

            existing = self.uow.review_log_repository.find_by_id(id)
            if existing is None:
                raise ReviewLogNotFoundError(id)

            # Safety: ensure the log belongs to this owner (since user_id is stored)
            if existing.user_id != owner_id:
                raise ReviewLogNotFoundError(id)

            # Optional safety: ensure the card is in the specified deck
            self._ensure_card_in_deck(existing.card_id, deck_id)

            self.uow.review_log_repository.delete_by_id(id)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise

    def delete_logs_by_card_id(self, card_id: int, deck_id: int, owner_id: int) -> None:
        """
        Delete all logs for a given card.
        (Usually admin/test-only; often handled by FK cascade when deleting the card.)
        """
        try:
            self.uow.begin()  # Explicitly start transaction
            self._ensure_deck_owned(deck_id, owner_id)
            self._ensure_card_in_deck(card_id, deck_id)

            self.uow.review_log_repository.delete_by_card_id(card_id)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise
