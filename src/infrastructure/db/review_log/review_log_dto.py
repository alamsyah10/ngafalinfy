from src.domain.model.review_log.review_log import ReviewLog
from src.infrastructure.db.review_log.review_log_table import ReviewLogTable
from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse


class ReviewLogDTO(ReviewLogTable):
    """
    ReviewLogDTO is a data transfer object associated with ReviewLog entity.
    """

    def to_entity(self) -> ReviewLog:
        return ReviewLog(
            id=self.id,
            card_id=self.card_id,
            user_id=self.user_id,
            ease_given=self.ease_given,
            prev_interval=self.prev_interval,
            new_interval=self.new_interval,
            prev_ease=self.prev_ease,
            new_ease=self.new_ease,
            reviewed_at=self.reviewed_at,
        )

    def to_response_model(self) -> ReviewLogDigestResponse:
        return ReviewLogDigestResponse(
            id=self.id,
            card_id=self.card_id,
            user_id=self.user_id,
            ease_given=self.ease_given,
            prev_interval=self.prev_interval,
            new_interval=self.new_interval,
            prev_ease=self.prev_ease,
            new_ease=self.new_ease,
            reviewed_at=self.reviewed_at,
        )

    @classmethod
    def from_entity(cls, log: ReviewLog) -> "ReviewLogDTO":
        return cls(
            id=log.id,
            card_id=log.card_id,
            user_id=log.user_id,
            ease_given=log.ease_given,
            prev_interval=log.prev_interval,
            new_interval=log.new_interval,
            prev_ease=log.prev_ease,
            new_ease=log.new_ease,
            reviewed_at=log.reviewed_at,
        )
