from abc import ABC, abstractmethod

from fastapi_pagination import Page

from src.usecase.deck.deck_schema import DeckDigestResponse


class DeckReadableService(ABC):
    """
    DeckReadableService defines a query service interface related Deck entity.
    """

    @abstractmethod
    def list_all_by_owner_id(self, owner_id: int) -> Page[DeckDigestResponse]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id_and_owner_id(
        self, id: int, owner_id: int
    ) -> DeckDigestResponse | None:
        raise NotImplementedError
