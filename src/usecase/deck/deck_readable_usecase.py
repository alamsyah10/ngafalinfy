from abc import ABC, abstractmethod

from fastapi_pagination import Page

from src.domain.model.deck.deck_exception import DeckNotFoundError
from src.usecase.deck.deck_schema import DeckDigestResponse

from .deck_readable_service import DeckReadableService


class DeckReadableUseCase(ABC):
    """
    DeckReadableUseCase defines a query usecase interface related User entity.
    """

    @abstractmethod
    def fetch_deck_by_id_and_owner_id(
        self, id: int, owner_id: int
    ) -> DeckDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def fetch_decks(self, owner_id: int) -> Page[DeckDigestResponse]:
        raise NotImplementedError


class DeckReadableUseCaseImpl(DeckReadableUseCase):
    """
    DeckReadableUseCaseImpl implements a query usecases related Deck entity.
    """

    def __init__(self, deck_service: DeckReadableService):
        self.deck_service: DeckReadableService = deck_service

    def fetch_deck_by_id_and_owner_id(
        self, id: int, owner_id: int
    ) -> DeckDigestResponse:
        try:
            deck = self.deck_service.find_by_id_and_owner_id(id, owner_id)
            if deck is None:
                raise DeckNotFoundError(id)
        except:
            raise

        return deck

    def fetch_decks(self, owner_id: int) -> Page[DeckDigestResponse]:
        try:
            decks = self.deck_service.list_all_by_owner_id(owner_id)
        except:
            raise

        return decks
