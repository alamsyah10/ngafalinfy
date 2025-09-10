from src.domain.model.deck.deck import Deck
from src.infrastructure.db.deck.deck_table import DeckTable
from src.usecase.deck.deck_schema import DeckDigestResponse


class DeckDTO(DeckTable):
    """
    DeckDTO is a data transfer object associated with Deck entity.
    """

    def to_entity(self) -> Deck:
        return Deck(
            id=self.id,
            name=self.name,
            owner_id=self.owner_id,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_response_model(self) -> DeckDigestResponse:
        return DeckDigestResponse(
            id=self.id,
            name=self.name,
            owner_id=self.owner_id,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, deck: Deck) -> "DeckDTO":
        return cls(
            id=deck.id,
            name=deck.name,
            owner_id=deck.owner_id,
            description=deck.description,
            created_at=deck.created_at,
            updated_at=deck.updated_at,
        )
