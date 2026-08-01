import logging
from abc import ABC, abstractmethod
from datetime import UTC, datetime

from src.domain.model.card.card import Card
from src.domain.model.card.card_exception import (
    CardNotFoundError,
    NoActiveCardsInDeckError,
)
from src.domain.model.deck.deck_exception import DeckNotFoundError
from src.domain.model.review_log.review_log import ReviewLog
from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.domain.repository.review_log import ReviewLogRepository
from src.usecase.card.card_schema import CardDigestResponse
from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse
from src.usecase.study.sm2 import sm2_schedule
from src.usecase.study.study_schema import (
    ReviewAnswerRequest,
    ReviewAnswerResponse,
    StudyNextResponse,
)

logger = logging.getLogger("backend")


class StudyWriteableUseCaseUnitOfWork(ABC):
    """
    StudyWriteableUseCaseUnitOfWork defines an interface based on Unit of Work pattern.
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


class StudyWriteableUseCase(ABC):
    """
    StudyWriteableUseCase defines command usecases related to study session.
    """

    @abstractmethod
    def fetch_next_due_card(self, deck_id: int, owner_id: int) -> StudyNextResponse:
        raise NotImplementedError

    @abstractmethod
    def answer_card(
        self,
        deck_id: int,
        card_id: int,
        owner_id: int,
        req: ReviewAnswerRequest,
    ) -> ReviewAnswerResponse:
        raise NotImplementedError


class StudyWriteableUseCaseImpl(StudyWriteableUseCase):
    """
    StudyWriteableUseCaseImpl implements command usecases for flashcard study flow:
    - Get next due card
    - Answer a card (update card scheduling + append review log)
    """

    def __init__(self, uow: StudyWriteableUseCaseUnitOfWork):
        self.uow = uow

    def _ensure_deck_owned(self, deck_id: int, owner_id: int) -> None:
        deck = self.uow.deck_repository.find_by_id_and_owner_id(deck_id, owner_id)
        if deck is None:
            raise DeckNotFoundError(deck_id)

    def _ensure_card_in_deck(self, card_id: int, deck_id: int) -> Card:
        card = self.uow.card_repository.find_by_id_and_deck_id(card_id, deck_id)
        if card is None:
            raise CardNotFoundError(card_id)
        return card

    def fetch_next_due_card(self, deck_id: int, owner_id: int) -> StudyNextResponse:
        """
        Get the next due card in a deck.
        """
        self._ensure_deck_owned(deck_id, owner_id)

        now = datetime.now(UTC)

        card = self.uow.card_repository.get_next_due_by_deck_id(
            deck_id=deck_id, now=now
        )
        if card is None:
            # MVP behavior: reuse existing error
            raise NoActiveCardsInDeckError(deck_id)

        return StudyNextResponse(card=CardDigestResponse.from_entity(card))

    def answer_card(
        self,
        deck_id: int,
        card_id: int,
        owner_id: int,
        req: ReviewAnswerRequest,
    ) -> ReviewAnswerResponse:
        """
        Apply SM-2 scheduling update to the card and append a review log.
        Both operations are committed atomically within one transaction.
        """
        try:
            self.uow.begin()  # Explicitly start transaction
            self._ensure_deck_owned(deck_id, owner_id)

            now = datetime.now(UTC)
            card = self._ensure_card_in_deck(card_id, deck_id)

            # Optional safety checks
            if not card.is_active or card.suspended:
                # keep behavior consistent with other endpoints
                raise CardNotFoundError(card_id)

            prev_ease = card.ease_factor
            prev_interval = card.interval
            prev_reps = card.repetitions
            prev_lapses = card.lapses

            res = sm2_schedule(
                now=now,
                quality=req.ease_given,
                prev_ease=prev_ease,
                prev_interval=prev_interval,
                prev_repetitions=prev_reps,
                prev_lapses=prev_lapses,
            )

            updated = card.update(
                ease_factor=res.new_ease,
                interval=res.new_interval,
                repetitions=res.new_repetitions,
                lapses=res.new_lapses,
                due_at=res.new_due_at,
            )

            self.uow.card_repository.update_card(updated)

            log = ReviewLog.new(
                card_id=card_id,
                user_id=owner_id,
                ease_given=req.ease_given,
                prev_interval=prev_interval,
                new_interval=res.new_interval,
                prev_ease=prev_ease,
                new_ease=res.new_ease,
                reviewed_at=now,
            )

            created_log = self.uow.review_log_repository.create_log(log)

            self.uow.commit()

        except Exception:
            self.uow.rollback()
            raise

        return ReviewAnswerResponse(
            card=CardDigestResponse.from_entity(updated),
            log=ReviewLogDigestResponse.from_entity(created_log),
        )
