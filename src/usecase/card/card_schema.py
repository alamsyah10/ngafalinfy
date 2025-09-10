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
    is_active: bool | None = Field(
        default=None, examples=[True], description="Activate/Deactivate this card"
    )


class CardDigestResponse(CustomBaseModel):
    id: int | None = Field(examples=[1], description="Card ID")
    deck_id: int = Field(examples=[1], description="Parent deck ID")
    front: str = Field(examples=["Hello"], description="Front text")
    back: str = Field(examples=["こんにちは"], description="Back text")
    notes: str | None = Field(default=None, description="Optional notes")
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
            is_active=card.is_active,
            created_at=card.created_at,
            updated_at=card.updated_at,
        )
