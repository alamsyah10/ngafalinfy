from datetime import datetime

from pydantic import Field

from src.domain.model.card.card import Card
from src.domain.model.common import CustomBaseModel


class CreateCardRequest(CustomBaseModel):
    front: str = Field(examples=["Hello"], description="Front text / question")
    back: str = Field(examples=["こんにちは"], description="Back text / answer")
    notes: str | None = Field(
        default=None, examples=["Polite greeting"], description="Optional notes"
    )


class UpdateCardRequest(CustomBaseModel):
    front: str | None = Field(
        default=None, examples=["Hi"], description="New front text"
    )
    back: str | None = Field(
        default=None, examples=["やあ"], description="New back text"
    )
    notes: str | None = Field(
        default=None, examples=["Casual usage"], description="New notes"
    )
    ease_factor: float | None = Field(
        default=None, examples=[2.5], description="Determines the ease of the card. The higher it is, the faster the review interval"
    )
    interval: int | None = Field(
        default=None, examples=[0], description="The number of days until the next review. Initially small, then increases according to the SM-2 algorithm"
    )
    repetitions: int | None = Field(
        default=None, examples=[0], description="Number of consecutive correct answers. Used to determine the learning phase (new, learning, review)"
    )
    lapses: int | None = Field(
        default=None, examples=[0], description="The number of times the user forgot to answer a card. Can be used for statistics and interval penalties"
    )
    due_at: datetime | None = Field(
        default=None, examples=["2025-09-02T12:34:56"], description="The due time of the next review. Becomes the query key to display 'due' cards"
    )
    suspended: bool | None = Field(
        default=None, examples=[False], description="If true, the card is suspended from the review session (e.g. paused by the user)"
    )
    is_active: bool | None = Field(
        default=None, examples=[True], description="Activate/Deactivate this card"
    )


class CardDigestResponse(CustomBaseModel):
    id: int | None = Field(examples=[1], description="Card ID")
    deck_id: int = Field(examples=[1], description="Parent deck ID")
    front: str = Field(examples=["Hello"], description="Front text")
    back: str = Field(examples=["こんにちは"], description="Back text")
    notes: str | None = Field(default=None, description="Optional notes")
    ease_factor: float = Field(examples=[2.5], description="Determines the ease of the card. The higher it is, the faster the review interval")
    interval: int = Field(examples=[0], description="The number of days until the next review. Initially small, then increases according to the SM-2 algorithm")
    repetitions: int = Field(examples=[0], description="Number of consecutive correct answers. Used to determine the learning phase (new, learning, review)")
    lapses: int = Field(examples=[0], description="The number of times the user forgot to answer a card. Can be used for statistics and interval penalties")
    due_at: datetime = Field(examples=["2025-09-02T12:34:56"], description="The due time of the next review. Becomes the query key to display 'due' cards")
    suspended: bool = Field(examples=[False], description="If true, the card is suspended from the review session (e.g. paused by the user)")
    is_active: bool = Field(examples=[True], description="Whether the card is active")
    created_at: datetime = Field(
        examples=["2025-09-02T12:34:56"], description="Creation timestamp"
    )
    updated_at: datetime = Field(
        examples=["2025-09-02T12:34:56"], description="Update timestamp"
    )

    @classmethod
    def from_entity(cls, card: Card) -> "CardDigestResponse":
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
