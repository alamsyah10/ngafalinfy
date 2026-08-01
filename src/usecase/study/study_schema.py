from pydantic import Field
from src.domain.model.common import CustomBaseModel
from src.usecase.card.card_schema import CardDigestResponse
from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse


class ReviewAnswerRequest(CustomBaseModel):
    ease_given: int = Field(ge=0, le=5, examples=[4], description="SM-2 quality 0..5")


class StudyNextResponse(CustomBaseModel):
    card: CardDigestResponse


class ReviewAnswerResponse(CustomBaseModel):
    card: CardDigestResponse
    log: ReviewLogDigestResponse
