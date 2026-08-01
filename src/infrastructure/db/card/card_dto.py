from src.domain.model.card.card import Card
from src.infrastructure.db.card.card_table import CardTable
from src.usecase.card.card_schema import CardDigestResponse


class CardDTO(CardTable):
    """
    CardDTO is a data transfer object associated with Card entity.
    """

    def to_entity(self) -> Card:
        return Card(
            id=self.id,
            deck_id=self.deck_id,
            front=self.front,
            back=self.back,
            notes=self.notes,
            ease_factor=self.ease_factor,
            interval=self.interval,
            repetitions=self.repetitions,
            lapses=self.lapses,
            due_at=self.due_at,
            suspended=self.suspended,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_response_model(self) -> CardDigestResponse:
        return CardDigestResponse(
            id=self.id,
            deck_id=self.deck_id,
            front=self.front,
            back=self.back,
            notes=self.notes,
            ease_factor=self.ease_factor,
            interval=self.interval,
            repetitions=self.repetitions,
            lapses=self.lapses,
            due_at=self.due_at,
            suspended=self.suspended,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, card: Card) -> "CardDTO":
        return cls(
            id=card.id,
            deck_id=card.deck_id,
            front=card.front,
            back=card.back,
            notes=card.notes,
            ease_factor=card.ease_factor,
            interval=card.interval,
            repetitions=card.repetitions,
            lapses=card.lapses,
            due_at=card.due_at,
            suspended=card.suspended,
            is_active=card.is_active,
            created_at=card.created_at,
            updated_at=card.updated_at,
        )
