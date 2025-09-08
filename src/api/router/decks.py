from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import PlainTextResponse
from fastapi_pagination import Page

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.deck import deck_read_usecase, deck_write_usecase
from src.api.error_schema.common import (
    ErrorMessageAuthorizationError,
    ErrorMessageInternalServerError,
    ErrorMessageResourceNotFoundError,
    ErrorMessageValidationError,
)
from src.usecase.deck.deck_readable_usecase import DeckReadableUseCase
from src.usecase.deck.deck_schema import (
    CreateDeckRequest,
    DeckDigestResponse,
    UpdateDeckRequest,
)
from src.usecase.deck.deck_writeable_usecase import DeckWriteableUseCase

router = APIRouter(prefix="/decks", tags=["decks"])


@router.post(
    "",
    response_model=DeckDigestResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_deck",
    summary="Create a deck",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorMessageValidationError,
            "description": "Bad Request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "Unauthorized",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "Internal Server Error",
        },
    },
)
def create_deck(
    payload: CreateDeckRequest,
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: DeckWriteableUseCase = Depends(deck_write_usecase),
):
    return usecase.create_deck(payload, user_id)


@router.put(
    "/{deck_id}",
    response_model=DeckDigestResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorMessageValidationError,
            "description": "Bad Request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "Internal Server Error",
        },
    },
    operation_id="update_deck",
    summary="Update a deck",
    description="Update a deck",
)
async def update_deck(
    deck_id: int = Path(..., description="Deck ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    payload: UpdateDeckRequest = Body(...),
    usecase: DeckWriteableUseCase = Depends(deck_write_usecase),
):
    return usecase.update_deck(deck_id, user_id, payload)


@router.delete(
    "/{deck_id}",
    response_class=PlainTextResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorMessageValidationError,
            "description": "Bad Request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "Internal Server Error",
        },
    },
    operation_id="delete_deck",
    summary="Delete a deck",
    description="Delete a deck",
)
async def delete_deck(
    deck_id: int = Path(..., description="Deck ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: DeckWriteableUseCase = Depends(deck_write_usecase),
):
    return usecase.delete_deck(deck_id, user_id)


@router.get(
    "",
    response_model=Page[DeckDigestResponse],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorMessageAuthorizationError,
            "description": "Unauthorized",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageInternalServerError,
            "description": "Internal Server Error",
        },
    },
    operation_id="get_my_decks",
    summary="List my decks",
)
def list_decks(
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: DeckReadableUseCase = Depends(deck_read_usecase),
) -> list[DeckDigestResponse]:
    return usecase.fetch_decks(user_id)
