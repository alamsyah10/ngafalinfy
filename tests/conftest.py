from datetime import datetime
from typing import cast

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi_pagination import Page, Params, create_page

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.card import card_read_usecase, card_write_usecase
from src.api.composition.deck import deck_read_usecase, deck_write_usecase
from src.api.router.cards import router as cards_router
from src.api.router.decks import router as decks_router
from src.domain.error.base import ResourceNotFoundError
from src.domain.model.deck.deck_exception import DeckNotFoundError
from src.usecase.card.card_readable_usecase import CardReadableUseCase
from src.usecase.card.card_schema import (
    CardDigestResponse,
    CreateCardRequest,
    UpdateCardRequest,
)
from src.usecase.card.card_writeable_usecase import CardWriteableUseCase
from src.usecase.deck.deck_readable_usecase import DeckReadableUseCase
from src.usecase.deck.deck_schema import (
    CreateDeckRequest,
    DeckDigestResponse,
    UpdateDeckRequest,
)
from src.usecase.deck.deck_writeable_usecase import DeckWriteableUseCase


class _FakeDeckReadable:
    def __init__(self):
        now = datetime.now()
        self._base = DeckDigestResponse(
            id=1,
            name="My Deck",
            owner_id=42,
            description="desc",
            created_at=now,
            updated_at=now,
        )

    def fetch_deck_by_id_and_owner_id(
        self, *, id: int, owner_id: int
    ) -> DeckDigestResponse:
        if id == 404:
            raise DeckNotFoundError(id)
        return self._base.model_copy(update={"id": id, "owner_id": owner_id})

    def fetch_decks(self, owner_id: int) -> Page[DeckDigestResponse]:
        # default pagination params (page=1, size=50) provided by Depends(Params) within fastapi-pagination
        # We return a ready Page via create_page to avoid needing add_pagination(app)
        items = [
            self._base.model_copy(update={"id": 1, "owner_id": owner_id}),
            self._base.model_copy(
                update={"id": 2, "owner_id": owner_id, "name": "Another Deck"}
            ),
        ]

        params = Params(page=1, size=50)
        return create_page(items, total=len(items), params=params)


class _FakeDeckWriteable:
    def __init__(self):
        now = datetime.now()
        self._base = DeckDigestResponse(
            id=999,
            name="Base",
            owner_id=42,
            description=None,
            created_at=now,
            updated_at=now,
        )

    def create_deck(
        self, deck_request: CreateDeckRequest, owner_id: int
    ) -> DeckDigestResponse:
        return self._base.model_copy(
            update={
                "id": 1001,
                "name": deck_request.name,
                "description": deck_request.description,
                "owner_id": owner_id,
            }
        )

    def update_deck(
        self, id: int, owner_id: int, deck: UpdateDeckRequest
    ) -> DeckDigestResponse:
        if id == 404:
            raise DeckNotFoundError(id)
        return self._base.model_copy(
            update={
                "id": id,
                "owner_id": owner_id,
                **deck.model_dump(exclude_none=True),
            }
        )

    def delete_deck(self, id: int, owner_id: int) -> None:
        if id == 404:
            raise DeckNotFoundError(id)
        return None


class _FakeCardReadable:
    def __init__(self):
        now = datetime.now()
        self._card = CardDigestResponse(
            id=123,
            deck_id=10,
            front="犬",
            back="いぬ",
            notes="dog",
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def fetch_card_by_id_and_deck_id(
        self, *, id: int, deck_id: int
    ) -> CardDigestResponse:
        return self._card.model_copy(update={"id": id, "deck_id": deck_id})

    def fetch_cards(
        self, *, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        items = [
            self._card.model_copy(
                update={"id": 1, "deck_id": deck_id, "is_active": True}
            ),
            self._card.model_copy(
                update={"id": 2, "deck_id": deck_id, "is_active": not only_active}
            ),
        ]
        return create_page(items, total=len(items), params=params)

    def fetch_recent_cards(
        self, *, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        base = self._card.model_copy(update={"deck_id": deck_id})
        items = [base.model_copy(update={"id": i}) for i in range(1, 6)]
        if only_active:
            items = [c.model_copy(update={"is_active": True}) for c in items]
        return create_page(items, total=len(items), params=params)

    def fetch_random_active_card(self, *, deck_id: int) -> CardDigestResponse:
        return self._card.model_copy(update={"deck_id": deck_id, "is_active": True})

    def fetch_card_count(self, *, deck_id: int, only_active: bool | None = None) -> int:
        if only_active is True:
            return 1
        if only_active is False:
            return 1
        return 2


class _FakeCardWriteable:
    def __init__(self):
        now = datetime.now()
        self._base = CardDigestResponse(
            id=999,
            deck_id=10,
            front="猫",
            back="ねこ",
            notes="cat",
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def create_card(
        self, *, deck_id: int, owner_id: int, req: CreateCardRequest
    ) -> CardDigestResponse:
        return self._base.model_copy(
            update={"id": 1001, "deck_id": deck_id, **req.model_dump()}
        )

    def update_card(
        self, *, id: int, deck_id: int, owner_id: int, req: UpdateCardRequest
    ) -> CardDigestResponse:
        return self._base.model_copy(
            update={"id": id, "deck_id": deck_id, **req.model_dump(exclude_none=True)}
        )

    def delete_card(self, *, id: int, deck_id: int, owner_id: int) -> None:
        return None


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()

    @app.exception_handler(ResourceNotFoundError)
    async def _not_found_handler(_, exc: ResourceNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"status": 404, "code": "not_found", "message": str(exc)},
        )

    app.include_router(cards_router)
    app.include_router(decks_router)

    # Dependency overrides (cast to satisfy type checker)
    app.dependency_overrides[get_current_user_id_usecase] = lambda: 42
    # DECK overrides (use the fakes; no DB)
    app.dependency_overrides[deck_read_usecase] = lambda: cast(
        DeckReadableUseCase, _FakeDeckReadable()
    )
    app.dependency_overrides[deck_write_usecase] = lambda: cast(
        DeckWriteableUseCase, _FakeDeckWriteable()
    )
    app.dependency_overrides[card_read_usecase] = lambda: cast(
        CardReadableUseCase, _FakeCardReadable()
    )
    app.dependency_overrides[card_write_usecase] = lambda: cast(
        CardWriteableUseCase, _FakeCardWriteable()
    )

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
