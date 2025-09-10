from datetime import datetime

from pydantic import Field

from src.domain.model.common import CustomBaseModel
from src.domain.model.deck.deck import Deck


class CreateDeckRequest(CustomBaseModel):
    name: str = Field(examples=["My Deck"], description="Deck name")
    description: str | None = Field(
        examples=["This is my deck"], description="Deck description"
    )


class UpdateDeckRequest(CustomBaseModel):
    name: str | None = Field(examples=["Updated Deck"], description="Deck name")
    description: str | None = Field(
        None, examples=["This is my updated deck"], description="Deck description"
    )


class DeckDigestResponse(CustomBaseModel):
    id: int | None = Field(examples=[1], description="Deck ID")
    name: str = Field(examples=["My Deck"], description="Deck name")
    owner_id: int = Field(examples=[1], description="Owner user ID")
    description: str | None = Field(
        examples=["This is my deck"], description="Deck description"
    )
    created_at: datetime = Field(
        examples=["2025-09-02T12:34:56"], description="Creation timestamp"
    )
    updated_at: datetime = Field(
        examples=["2025-09-02T12:34:56"], description="Update timestamp"
    )

    @classmethod
    def from_entity(cls, deck: Deck) -> "DeckDigestResponse":
        return cls(
            id=deck.id,
            name=deck.name,
            owner_id=deck.owner_id,
            description=deck.description,
            created_at=deck.created_at,
            updated_at=deck.updated_at,
        )
