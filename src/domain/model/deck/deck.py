from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class Deck:
    id: int | None = None
    name: str = field(compare=False)
    owner_id: int
    description: str | None = field(default=None, compare=False)
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    def get_id(self) -> int | None:
        return self.id

    def update(
        self,
        name: str | None = None,
        description: str | None = None,
    ):
        new_name = name if name is not None else self.name
        new_description = description if description is not None else self.description

        return Deck(
            id=self.id,
            name=new_name,
            owner_id=self.owner_id,
            description=new_description,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    @classmethod
    def new(
        cls,
        name: str,
        owner_id: int,
        description: str | None,
    ) -> "Deck":
        return cls(id=0, name=name, owner_id=owner_id, description=description)
