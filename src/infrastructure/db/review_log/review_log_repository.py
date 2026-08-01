from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.domain.model.review_log.review_log import ReviewLog
from src.domain.repository.review_log import ReviewLogRepository
from src.infrastructure.db.review_log.review_log_dto import ReviewLogDTO


class ReviewLogRepositoryImpl(ReviewLogRepository):
    """
    ReviewLogRepositoryImpl implements CRUD & simple queries for ReviewLog entity.
    Review logs are usually append-only (immutable), so "update" is intentionally omitted.
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def create_log(self, log: ReviewLog) -> ReviewLog:
        dto = ReviewLogDTO.from_entity(log)
        try:
            self.session.add(dto)
            # Flush so dto.id becomes available without committing
            self.session.flush()
        except Exception:
            raise

        # Return entity with generated id if needed
        return dto.to_entity()

    def find_by_id(self, id: int) -> ReviewLog | None:
        try:
            dto = self.session.query(ReviewLogDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except Exception:
            raise
        return dto.to_entity()

    def delete_by_id(self, id: int) -> None:
        try:
            self.session.query(ReviewLogDTO).filter_by(id=id).delete()
        except Exception:
            raise

    def list_by_card_id(
        self,
        card_id: int,
        limit: int | None = None,
        newest_first: bool = True,
    ) -> list[ReviewLog]:
        q = self.session.query(ReviewLogDTO).filter_by(card_id=card_id)
        q = q.order_by(
            ReviewLogDTO.reviewed_at.desc()
            if newest_first
            else ReviewLogDTO.reviewed_at.asc()
        )
        if limit is not None:
            q = q.limit(limit)
        return [dto.to_entity() for dto in q.all()]

    def get_latest_by_card_id(self, card_id: int) -> ReviewLog | None:
        dto = (
            self.session.query(ReviewLogDTO)
            .filter_by(card_id=card_id)
            .order_by(ReviewLogDTO.reviewed_at.desc())
            .limit(1)
            .first()
        )
        return dto.to_entity() if dto else None

    def list_by_deck_id(
        self,
        deck_id: int,
        limit: int | None = None,
        newest_first: bool = True,
    ) -> list[ReviewLog]:
        """
        Requires a join from review_logs -> cards to filter by deck_id.
        Assumes ReviewLogTable.card_id FK points to CardTable.id,
        and CardDTO maps to CardTable (table name "cards").
        """
        # Local import to avoid circular dependency if your project structure causes it
        from src.infrastructure.db.card.card_dto import CardDTO

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
        if limit is not None:
            q = q.limit(limit)

        return [dto.to_entity() for dto in q.all()]

    def delete_by_card_id(self, card_id: int) -> None:
        try:
            self.session.query(ReviewLogDTO).filter_by(card_id=card_id).delete()
        except Exception:
            raise
