from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.responses import PlainTextResponse
from fastapi_pagination import Page, Params

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.card import card_read_usecase, card_write_usecase
from src.api.error_schema.common import (
    ErrorMessageAuthorizationError,
    ErrorMessageInternalServerError,
    ErrorMessageResourceNotFoundError,
    ErrorMessageValidationError,
)
from src.usecase.card.card_readable_usecase import CardReadableUseCase
from src.usecase.card.card_schema import (
    CardDigestResponse,
    CreateCardRequest,
    UpdateCardRequest,
)
from src.usecase.card.card_writeable_usecase import CardWriteableUseCase

router = APIRouter(prefix="/decks/{deck_id:int}/cards", tags=["cards"])


@router.get(
    "/random",
    response_model=CardDigestResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_random_active_card",
    summary="Get a random active card from a deck",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError
        },
    },
)
def get_random_active_card(
    deck_id: int = Path(..., description="Deck ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: CardReadableUseCase = Depends(card_read_usecase),
) -> CardDigestResponse:
    return usecase.fetch_random_active_card(deck_id=deck_id)


@router.post(
    "",
    response_model=CardDigestResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_card",
    summary="Create a card",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessageValidationError},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError
        },
    },
)
def create_card(
    deck_id: int = Path(..., description="Deck ID"),
    payload: CreateCardRequest = Body(...),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: CardWriteableUseCase = Depends(card_write_usecase),
) -> CardDigestResponse:
    return usecase.create_card(deck_id=deck_id, owner_id=user_id, req=payload)


@router.get(
    "",
    response_model=Page[CardDigestResponse],
    status_code=status.HTTP_200_OK,
    operation_id="list_cards",
    summary="List cards in a deck",
)
def list_cards(
    deck_id: int = Path(..., description="Deck ID"),
    params: Params = Depends(),
    only_active: bool = Query(True, description="Return only active cards"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: CardReadableUseCase = Depends(card_read_usecase),
) -> Page[CardDigestResponse]:
    return usecase.fetch_cards(deck_id=deck_id, params=params, only_active=only_active)


@router.get(
    "/{card_id:int}",
    response_model=CardDigestResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_card",
    summary="Get a card by ID (within a deck)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError
        },
    },
)
def get_card(
    deck_id: int = Path(..., description="Deck ID"),
    card_id: int = Path(..., description="Card ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: CardReadableUseCase = Depends(card_read_usecase),
) -> CardDigestResponse:
    return usecase.fetch_card_by_id_and_deck_id(id=card_id, deck_id=deck_id)


@router.put(
    "/{card_id:int}",
    response_model=CardDigestResponse,
    status_code=status.HTTP_200_OK,
    operation_id="update_card",
    summary="Update a card",
)
def update_card(
    deck_id: int = Path(..., description="Deck ID"),
    card_id: int = Path(..., description="Card ID"),
    payload: UpdateCardRequest = Body(...),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: CardWriteableUseCase = Depends(card_write_usecase),
) -> CardDigestResponse:
    return usecase.update_card(
        id=card_id, deck_id=deck_id, owner_id=user_id, req=payload
    )


@router.delete(
    "/{card_id:int}",
    response_class=PlainTextResponse,
    status_code=status.HTTP_202_ACCEPTED,
    operation_id="delete_card",
    summary="Delete a card",
)
def delete_card(
    deck_id: int = Path(..., description="Deck ID"),
    card_id: int = Path(..., description="Card ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: CardWriteableUseCase = Depends(card_write_usecase),
):
    usecase.delete_card(id=card_id, deck_id=deck_id, owner_id=user_id)
    return PlainTextResponse("Accepted", status_code=status.HTTP_202_ACCEPTED)
