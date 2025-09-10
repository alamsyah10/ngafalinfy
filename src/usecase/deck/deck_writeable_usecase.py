import logging
from abc import ABC, abstractmethod

from src.domain.model.deck.deck import Deck
from src.domain.model.deck.deck_exception import DeckNotFoundError
from src.domain.repository.deck import DeckRepository
from src.usecase.deck.deck_schema import (
    CreateDeckRequest,
    DeckDigestResponse,
    UpdateDeckRequest,
)

logger = logging.getLogger("backend")


class DeckWriteableUseCaseUnitOfWork(ABC):
    """
    DeckWritableUseCaseUnitOfWork defines an interface based on Unit of Work pattern.
    """

    deck_repository: DeckRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class DeckWriteableUseCase:
    """
    DeckWritableUseCase defines a command usecase interface related Deck entity.
    """

    @abstractmethod
    def create_deck(
        self, deck_request: CreateDeckRequest, owner_id: int
    ) -> DeckDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def update_deck(
        self, id: int, owner_id: int, deck: UpdateDeckRequest
    ) -> DeckDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_deck(self, id: int, owner_id: int) -> None:
        raise NotImplementedError


class DeckWriteableUseCaseImpl(DeckWriteableUseCase):
    """
    DeckWritableUseCaseImpl implements a command usecases related Deck entity.
    """

    def __init__(self, uow: DeckWriteableUseCaseUnitOfWork):
        self.uow = uow

    def create_deck(
        self, deck_request: CreateDeckRequest, owner_id: int
    ) -> DeckDigestResponse:
        try:
            deck = Deck.new(
                name=deck_request.name,
                owner_id=owner_id,
                description=deck_request.description,
            )
            self.uow.deck_repository.create_deck(deck)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return DeckDigestResponse.from_entity(deck)

    def update_deck(
        self, id: int, owner_id: int, deck: UpdateDeckRequest
    ) -> DeckDigestResponse:
        try:
            existing_deck = self.uow.deck_repository.find_by_id_and_owner_id(
                id, owner_id
            )
            if existing_deck is None:
                raise DeckNotFoundError(id)

            deck_updated = existing_deck.update(
                name=deck.name, description=deck.description
            )

            self.uow.deck_repository.update_deck(deck_updated)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return DeckDigestResponse.from_entity(deck_updated)

    def delete_deck(self, id: int, owner_id: int):
        try:
            existing_dataset = self.uow.deck_repository.find_by_id_and_owner_id(
                id, owner_id
            )
            if existing_dataset is None:
                raise DeckNotFoundError(id)

            self.uow.deck_repository.delete_deck_by_id_and_owner_id(id, owner_id)
            self.uow.commit()

        except:
            self.uow.rollback()
            raise
