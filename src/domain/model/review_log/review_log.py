from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class ReviewLog:
    id: int | None = None

    card_id: int
    user_id: int

    ease_given: int = field(compare=False)

    prev_interval: int = field(compare=False)
    new_interval: int = field(compare=False)

    prev_ease: float = field(compare=False)
    new_ease: float = field(compare=False)

    reviewed_at: datetime = field(default_factory=datetime.now, compare=False)

    def get_id(self) -> int | None:
        return self.id

    @classmethod
    def new(
        cls,
        *,
        card_id: int,
        user_id: int,
        ease_given: int,
        prev_interval: int,
        new_interval: int,
        prev_ease: float,
        new_ease: float,
        reviewed_at: datetime | None = None,
    ) -> "ReviewLog":
        return cls(
            id=0,
            card_id=card_id,
            user_id=user_id,
            ease_given=ease_given,
            prev_interval=prev_interval,
            new_interval=new_interval,
            prev_ease=prev_ease,
            new_ease=new_ease,
            reviewed_at=reviewed_at if reviewed_at is not None else datetime.now(UTC),
        )
