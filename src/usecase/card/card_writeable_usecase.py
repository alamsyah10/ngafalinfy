import logging
from abc import ABC, abstractmethod

from src.domain.model.card.card import Card
from src.domain.model.card.card_exception import CardNotFoundError
from src.domain.model.deck.deck_exception import DeckNotFoundError
from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.usecase.card.card_schema import (
    CardDigestResponse,
    CreateCardRequest,
    UpdateCardRequest,
)

logger = logging.getLogger("backend")


class CardWriteableUseCaseUnitOfWork(ABC):
    """
    CardWritableUseCaseUnitOfWork defines an interface based on Unit of Work pattern.
    """

    deck_repository: DeckRepository
    card_repository: CardRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class CardWriteableUseCase(ABC):
    """
    CardWritableUseCase defines command usecases related to Card entity.
    """

    @abstractmethod
    def create_card(
        self, deck_id: int, owner_id: int, req: CreateCardRequest
    ) -> CardDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def update_card(
        self, id: int, deck_id: int, owner_id: int, req: UpdateCardRequest
    ) -> CardDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_card(self, id: int, deck_id: int, owner_id: int) -> None:
        raise NotImplementedError


class CardWriteableUseCaseImpl(CardWriteableUseCase):
    """
    CardWritableUseCaseImpl implements command usecases related to Card entity.
    """

    def __init__(self, uow: CardWriteableUseCaseUnitOfWork):
        self.uow = uow

    def _ensure_deck_owned(self, deck_id: int, owner_id: int):
        deck = self.uow.deck_repository.find_by_id_and_owner_id(deck_id, owner_id)
        if deck is None:
            raise DeckNotFoundError(deck_id)

    def create_card(
        self, deck_id: int, owner_id: int, req: CreateCardRequest
    ) -> CardDigestResponse:
        try:
            self._ensure_deck_owned(deck_id, owner_id)

            card = Card.new(
                deck_id=deck_id,
                front=req.front,
                back=req.back,
                notes=req.notes,
            )

            self.uow.card_repository.create_card(card)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise

        return CardDigestResponse.from_entity(card)

    def update_card(
        self, id: int, deck_id: int, owner_id: int, req: UpdateCardRequest
    ) -> CardDigestResponse:
        try:
            self._ensure_deck_owned(deck_id, owner_id)

            existing = self.uow.card_repository.find_by_id_and_deck_id(id, deck_id)
            if existing is None:
                raise CardNotFoundError(id)

            updated = existing.update(
                front=req.front,
                back=req.back,
                notes=req.notes,
                is_active=req.is_active,
            )

            self.uow.card_repository.update_card(updated)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise

        return CardDigestResponse.from_entity(updated)

    def delete_card(self, id: int, deck_id: int, owner_id: int) -> None:
        try:
            self._ensure_deck_owned(deck_id, owner_id)

            existing = self.uow.card_repository.find_by_id_and_deck_id(id, deck_id)
            if existing is None:
                raise CardNotFoundError(id)

            self.uow.card_repository.delete_card_by_id_and_deck_id(id, deck_id)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise
