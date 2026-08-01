from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src.infrastructure.db.card.card_dto import CardDTO
from src.infrastructure.db.review_log.review_log_dto import ReviewLogDTO
from src.usecase.review_log.review_log_readable_service import ReviewLogReadableService
from src.usecase.review_log.review_log_schema import ReviewLogDigestResponse


class ReviewLogReadableServiceImpl(ReviewLogReadableService):
    """
    ReviewLogReadableServiceImpl implements READ operations related
    ReviewLog entity using SQLAlchemy
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def list_all_by_card_id(
        self,
        card_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        q = self.session.query(ReviewLogDTO).filter_by(card_id=card_id)
        q = q.order_by(
            ReviewLogDTO.reviewed_at.desc()
            if newest_first
            else ReviewLogDTO.reviewed_at.asc()
        )

        return paginate(
            q,
            params=params,
            transformer=lambda dtos: [dto.to_response_model() for dto in dtos],
        )

    def list_all_by_deck_id(
        self,
        deck_id: int,
        params: Params,
        newest_first: bool = True,
    ) -> Page[ReviewLogDigestResponse]:
        q = (
            self.session.query(ReviewLogDTO)
            .join(CardDTO, ReviewLogDTO.card_id == CardDTO.id)
            .filter(CardDTO.deck_id == deck_id)
        )
        q = q.order_by(
            ReviewLogDTO.reviewed_at.desc()
            if newest_first
            else ReviewLogDTO.reviewed_at.asc()
        )

        return paginate(
            q,
            params=params,
            transformer=lambda dtos: [dto.to_response_model() for dto in dtos],
        )

    def find_by_id(self, id: int) -> ReviewLogDigestResponse | None:
        dto = self.session.query(ReviewLogDTO).filter_by(id=id).one_or_none()
        return dto.to_response_model() if dto else None

    def get_latest_by_card_id(self, card_id: int) -> ReviewLogDigestResponse | None:
        dto = (
            self.session.query(ReviewLogDTO)
            .filter_by(card_id=card_id)
            .order_by(ReviewLogDTO.reviewed_at.desc())
            .limit(1)
            .first()
        )
        return dto.to_response_model() if dto else None

    def count_by_card_id(self, card_id: int) -> int:
        return self.session.query(ReviewLogDTO).filter_by(card_id=card_id).count()

    def count_by_deck_id(self, deck_id: int) -> int:
        return (
            self.session.query(ReviewLogDTO)
            .join(CardDTO, ReviewLogDTO.card_id == CardDTO.id)
            .filter(CardDTO.deck_id == deck_id)
            .count()
        )
