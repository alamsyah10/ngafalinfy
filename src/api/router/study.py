from fastapi import APIRouter, Body, Depends, Path, status

from src.api.composition.auth import get_current_user_id_usecase
from src.api.composition.study import study_write_usecase
from src.api.error_schema.common import (
    ErrorMessageAuthorizationError,
    ErrorMessageInternalServerError,
    ErrorMessageResourceNotFoundError,
    ErrorMessageValidationError,
)
from src.usecase.study.study_schema import (
    ReviewAnswerRequest,
    ReviewAnswerResponse,
    StudyNextResponse,
)
from src.usecase.study.study_writeable_usecase import StudyWriteableUseCase

router = APIRouter(prefix="/decks/{deck_id:int}/study", tags=["study"])


@router.get(
    "/next",
    response_model=StudyNextResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_next_due_card",
    summary="Get next due card in a deck",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessageInternalServerError},
    },
)
def get_next_due_card(
    deck_id: int = Path(..., description="Deck ID"),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: StudyWriteableUseCase = Depends(study_write_usecase),
) -> StudyNextResponse:
    return usecase.fetch_next_due_card(deck_id=deck_id, owner_id=user_id)


@router.post(
    "/{card_id:int}/answer",
    response_model=ReviewAnswerResponse,
    status_code=status.HTTP_200_OK,
    operation_id="answer_card",
    summary="Answer a card (update scheduling + create review log)",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessageValidationError},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessageAuthorizationError},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessageResourceNotFoundError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorMessageInternalServerError},
    },
)
def answer_card(
    deck_id: int = Path(..., description="Deck ID"),
    card_id: int = Path(..., description="Card ID"),
    payload: ReviewAnswerRequest = Body(...),
    user_id: int = Depends(get_current_user_id_usecase),
    usecase: StudyWriteableUseCase = Depends(study_write_usecase),
) -> ReviewAnswerResponse:
    return usecase.answer_card(
        deck_id=deck_id,
        card_id=card_id,
        owner_id=user_id,
        req=payload,
    )
