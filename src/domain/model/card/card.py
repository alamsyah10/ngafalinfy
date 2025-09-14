from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class Card:
    id: int | None = None
    deck_id: int
    front: str = field(compare=False)
    back: str = field(compare=False)
    notes: str | None = field(default=None, compare=False)
    ease_factor: float = field(default=2.5)
    interval: int = field(default=0)
    repetitions: int = field(default=0)
    lapses: int = field(default=0)
    due_at: datetime = field(default=datetime.now())
    suspended: bool = False
    is_active: bool = True
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    def get_id(self) -> int | None:
        return self.id

    def update(
        self,
        front: str | None = None,
        back: str | None = None,
        notes: str | None = None,
        ease_factor: float | None = None,
        interval: int | None = None,
        repetitions: int | None = None,
        lapses: int | None = None,
        due_at: datetime | None = None,
        suspended: bool | None = None,
        is_active: bool | None = None,
    ) -> "Card":
        return Card(
            id=self.id,
            deck_id=self.deck_id,
            front=front if front is not None else self.front,
            back=back if back is not None else self.back,
            notes=notes if notes is not None else self.notes,
            ease_factor=ease_factor if ease_factor is not None else self.ease_factor,
            interval=interval if interval is not None else self.interval,
            repetitions=repetitions if repetitions is not None else self.repetitions,
            lapses=lapses if lapses is not None else self.lapses,
            due_at=due_at if due_at is not None else self.due_at,
            suspended=suspended if suspended is not None else self.suspended,
            is_active=is_active if is_active is not None else self.is_active,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    @classmethod
    def new(
        cls,
        deck_id: int,
        front: str,
        back: str,
        notes: str | None = None,
    ) -> "Card":
        return cls(id=0, deck_id=deck_id, front=front, back=back, notes=notes)
