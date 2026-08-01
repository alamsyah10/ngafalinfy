from datetime import datetime

from pydantic import Field

from src.domain.model.common import CustomBaseModel
from src.domain.model.review_log.review_log import ReviewLog


class ReviewLogDigestResponse(CustomBaseModel):
    id: int | None = Field(examples=[1], description="Review log ID")
    card_id: int = Field(examples=[1], description="Reviewed card ID")
    user_id: int = Field(examples=[1], description="Reviewer user ID")

    ease_given: int = Field(
        examples=[4],
        description="User's review grade (quality) for SM-2. Typically 0..5 (e.g., 0=forgot, 3=hard, 4=good, 5=easy)",
    )

    prev_interval: int = Field(
        examples=[1],
        description="Previous interval (days) before applying scheduling update",
    )
    new_interval: int = Field(
        examples=[6],
        description="New interval (days) after applying scheduling update",
    )

    prev_ease: float = Field(
        examples=[2.5],
        description="Previous ease factor before review (SM-2 ease factor)",
    )
    new_ease: float = Field(
        examples=[2.6],
        description="New ease factor after review (SM-2 ease factor)",
    )

    reviewed_at: datetime = Field(
        examples=["2025-09-02T12:34:56"],
        description="Timestamp when the review happened",
    )

    @classmethod
    def from_entity(cls, log: ReviewLog) -> "ReviewLogDigestResponse":
        return cls(
            id=log.id,
            card_id=log.card_id,
            user_id=log.user_id,
            ease_given=log.ease_given,
            prev_interval=log.prev_interval,
            new_interval=log.new_interval,
            prev_ease=log.prev_ease,
            new_ease=log.new_ease,
            reviewed_at=log.reviewed_at,
        )
