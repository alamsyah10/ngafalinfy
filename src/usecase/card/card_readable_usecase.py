from abc import ABC, abstractmethod

from fastapi_pagination import Page, Params

from src.domain.model.card.card_exception import (
    CardNotFoundError,
    NoActiveCardsInDeckError,
)
from src.usecase.card.card_schema import CardDigestResponse

from .card_readable_service import CardReadableService


class CardReadableUseCase(ABC):
    """
    CardReadableUseCase defines a query usecase interface related Card entity.
    """

    @abstractmethod
    def fetch_card_by_id_and_deck_id(self, id: int, deck_id: int) -> CardDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def fetch_cards(
        self, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        raise NotImplementedError

    @abstractmethod
    def fetch_random_active_card(self, deck_id: int) -> CardDigestResponse:
        raise NotImplementedError

    @abstractmethod
    def fetch_card_count(self, deck_id: int, only_active: bool | None = None) -> int:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_cards(
        self, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        raise NotImplementedError


class CardReadableUseCaseImpl(CardReadableUseCase):
    """
    CardReadableUseCaseImpl implements query usecases related to Card entity.
    """

    def __init__(self, card_service: CardReadableService):
        self.card_service: CardReadableService = card_service

    def fetch_card_by_id_and_deck_id(self, id: int, deck_id: int) -> CardDigestResponse:
        card = self.card_service.find_by_id_and_deck_id(id, deck_id)
        if card is None:
            raise CardNotFoundError(id)
        return card

    def fetch_cards(
        self, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        return self.card_service.list_all_by_deck_id(
            deck_id, params, only_active=only_active
        )

    def fetch_random_active_card(self, deck_id: int) -> CardDigestResponse:
        card = self.card_service.get_random_active_by_deck_id(deck_id)
        if card is None:
            raise NoActiveCardsInDeckError(deck_id)
        return card

    def fetch_card_count(self, deck_id: int, only_active: bool | None = None) -> int:
        return self.card_service.count_by_deck_id(deck_id, only_active=only_active)

    def fetch_recent_cards(
        self, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        return self.card_service.list_recent_by_deck_id(
            deck_id, params, only_active=only_active
        )
