from datetime import datetime

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.responses import PlainTextResponse
from fastapi_pagination import Page, Params
from pydantic import Field

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.review_log import (
    review_log_read_usecase,
    review_log_write_usecase,
)
from src.api.error_schema.common import (
    ErrorMessageAuthorizationError,
    ErrorMessageInternalServerError,
    ErrorMessageResourceNotFoundError,
    ErrorMessageValidationError,
)
from src.domain.model.common import CustomBaseModel
from src.usecase.review_log.review_log_readable_usecase import ReviewLogReadableUseCase
from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse
from src.usecase.review_log.review_log_writeable_usecase import ReviewLogWriteableUseCase

router = APIRouter(prefix="/decks/{deck_id:int}/review-logs", tags=["review-logs"])


class CreateReviewLogRequest(CustomBaseModel):
    card_id: int = Field(examples=[1], description="Reviewed card ID")
    ease_given: int = Field(
        examples=[4],
        description="User's review grade (quality) for SM-2. Typically 0..5",
        ge=0,
        le=5,
    )
    prev_interval: int = Field(
        examples=[1],
        description="Previous interval (days) before scheduling update",
        ge=0,
    )
    new_interval: int = Field(
        examples=[6],
        description="New interval (days) after scheduling update",
        ge=0,
    )
    prev_ease: float = Field(
        examples=[2.5],
        description="Previous ease factor before review",
    )
    new_ease: float = Field(
        examples=[2.6],
        description="New ease factor after review",
    )
    reviewed_at: datetime | None = Field(
        default=None,
        examples=["2025-09-02T12:34:56"],
        description="Optional timestamp (defaults to now)",
    )


@router.post(
    "",
    response_model=ReviewLogDigestResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_review_log",
    summary="Create a review log (append-only history)",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessageValidationError},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessageInternalServerError},
    },
)
def create_review_log(
    deck_id: int = Path(..., description="Deck ID"),
    payload: CreateReviewLogRequest = Body(...),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: ReviewLogWriteableUseCase = Depends(review_log_write_usecase),
) -> ReviewLogDigestResponse:
    return usecase.create_log(
        deck_id=deck_id,
        card_id=payload.card_id,
        owner_id=user_id,
        ease_given=payload.ease_given,
        prev_interval=payload.prev_interval,
        new_interval=payload.new_interval,
        prev_ease=payload.prev_ease,
        new_ease=payload.new_ease,
        reviewed_at=payload.reviewed_at,
    )


@router.get(
    "",
    response_model=Page[ReviewLogDigestResponse],
    status_code=status.HTTP_200_OK,
    operation_id="list_review_logs",
    summary="List review logs in a deck",
)
def list_review_logs(
    deck_id: int = Path(..., description="Deck ID"),
    params: Params = Depends(),
    newest_first: bool = Query(True, description="Sort by reviewed_at desc"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: ReviewLogReadableUseCase = Depends(review_log_read_usecase),
) -> Page[ReviewLogDigestResponse]:
    return usecase.fetch_logs_by_deck_id(
        deck_id=deck_id,
        params=params,
        newest_first=newest_first,
    )


@router.get(
    "/{review_log_id:int}",
    response_model=ReviewLogDigestResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_review_log",
    summary="Get a review log by ID",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessageInternalServerError},
    },
)
def get_review_log(
    deck_id: int = Path(..., description="Deck ID"),
    review_log_id: int = Path(..., description="Review log ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: ReviewLogReadableUseCase = Depends(review_log_read_usecase),
) -> ReviewLogDigestResponse:
    # Note: deck_id is kept in the path for consistency with other routers.
    # Ownership checks are handled by the usecase/service layer patterns you already use.
    return usecase.fetch_log_by_id(review_log_id)


@router.get(
    "/cards/{card_id:int}",
    response_model=Page[ReviewLogDigestResponse],
    status_code=status.HTTP_200_OK,
    operation_id="list_review_logs_by_card",
    summary="List review logs for a card (within a deck)",
)
def list_review_logs_by_card(
    deck_id: int = Path(..., description="Deck ID"),
    card_id: int = Path(..., description="Card ID"),
    params: Params = Depends(),
    newest_first: bool = Query(True, description="Sort by reviewed_at desc"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: ReviewLogReadableUseCase = Depends(review_log_read_usecase),
) -> Page[ReviewLogDigestResponse]:
    return usecase.fetch_logs_by_card_id(
        card_id=card_id,
        params=params,
        newest_first=newest_first,
    )


@router.get(
    "/cards/{card_id:int}/latest",
    response_model=ReviewLogDigestResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_latest_review_log_by_card",
    summary="Get the latest review log for a card",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessageInternalServerError},
    },
)
def get_latest_review_log_by_card(
    deck_id: int = Path(..., description="Deck ID"),
    card_id: int = Path(..., description="Card ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: ReviewLogReadableUseCase = Depends(review_log_read_usecase),
) -> ReviewLogDigestResponse:
    return usecase.fetch_latest_log_by_card_id(card_id=card_id)


@router.delete(
    "/{review_log_id:int}",
    response_class=PlainTextResponse,
    status_code=status.HTTP_202_ACCEPTED,
    operation_id="delete_review_log",
    summary="Delete a review log (admin/test use)",
)
def delete_review_log(
    deck_id: int = Path(..., description="Deck ID"),
    review_log_id: int = Path(..., description="Review log ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: ReviewLogWriteableUseCase = Depends(review_log_write_usecase),
):
    usecase.delete_log(id=review_log_id, deck_id=deck_id, owner_id=user_id)
    return PlainTextResponse("Accepted", status_code=status.HTTP_202_ACCEPTED)
