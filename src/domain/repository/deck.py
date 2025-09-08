from abc import ABC, abstractmethod

from src.domain.model.deck.deck import Deck


class DeckRepository(ABC):
    """
    DeckRepository defines a repository interface for Deck entity.
    """

    @abstractmethod
    def create_deck(self, deck: Deck):
        raise NotImplementedError

    @abstractmethod
    def update_deck(self, deck: Deck):
        raise NotImplementedError

    @abstractmethod
    def delete_deck_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int, with_relation: bool = False) -> Deck | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id_and_owner_id(
        self, id: int, owner_id: int, with_relation: bool = False
    ) -> Deck | None:
        raise NotImplementedError

    @abstractmethod
    def delete_deck_by_id_and_owner_id(self, id: int, owner_id: int):
        raise NotImplementedError
