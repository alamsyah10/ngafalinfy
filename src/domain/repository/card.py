from abc import ABC, abstractmethod

from src.domain.model.card.card import Card


class CardRepository(ABC):
    """
    CardRepository defines a repository interface for Card entity.
    """

    @abstractmethod
    def create_card(self, card: Card):
        raise NotImplementedError

    @abstractmethod
    def update_card(self, card: Card):
        raise NotImplementedError

    @abstractmethod
    def delete_card_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int, with_relation: bool = False) -> Card | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id_and_deck_id(
        self, id: int, deck_id: int, with_relation: bool = False
    ) -> Card | None:
        raise NotImplementedError

    @abstractmethod
    def delete_card_by_id_and_deck_id(self, id: int, deck_id: int):
        raise NotImplementedError

    @abstractmethod
    def list_by_deck_id(self, deck_id: int, only_active: bool = False) -> list[Card]:
        raise NotImplementedError

    @abstractmethod
    def get_random_active_by_deck_id(self, deck_id: int) -> Card | None:
        raise NotImplementedError
