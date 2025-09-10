from abc import ABC, abstractmethod

from fastapi_pagination import Page, Params

from src.usecase.card.card_schema import CardDigestResponse


class CardReadableService(ABC):
    """
    CardReadableService defines a query service interface related Card entity.
    """

    @abstractmethod
    def list_all_by_deck_id(
        self,
        deck_id: int,
        params: Params,
        only_active: bool = False,
    ) -> Page[CardDigestResponse]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id_and_deck_id(
        self,
        id: int,
        deck_id: int,
    ) -> CardDigestResponse | None:
        raise NotImplementedError

    @abstractmethod
    def get_random_active_by_deck_id(self, deck_id: int) -> CardDigestResponse | None:
        raise NotImplementedError

    @abstractmethod
    def count_by_deck_id(self, deck_id: int, only_active: bool | None = None) -> int:
        raise NotImplementedError

    @abstractmethod
    def list_recent_by_deck_id(
        self, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        raise NotImplementedError
