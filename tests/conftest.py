from datetime import datetime
from typing import cast

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi_pagination import Page, Params, create_page

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.card import card_read_usecase, card_write_usecase
from src.api.router.cards import router as cards_router
from src.domain.error.base import ResourceNotFoundError
from src.usecase.card.card_readable_usecase import CardReadableUseCase
from src.usecase.card.card_schema import (
    CardDigestResponse,
    CreateCardRequest,
    UpdateCardRequest,
)
from src.usecase.card.card_writeable_usecase import CardWriteableUseCase


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

    # Dependency overrides (cast to satisfy type checker)
    app.dependency_overrides[get_current_user_id_usecase] = lambda: 1
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
