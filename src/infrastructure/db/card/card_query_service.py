from datetime import datetime, timezone

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.infrastructure.db.card.card_dto import CardDTO
from src.usecase.card.card_readable_service import CardReadableService
from src.usecase.card.card_schema import CardDigestResponse, DeckStatsResponse


class CardReadableServiceImpl(CardReadableService):
    """
    CardReadableServiceImpl implements READ operations related
    Card entity using SQLAlchemy.
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def list_all_by_deck_id(
        self,
        deck_id: int,
        params: Params,
        only_active: bool = False,
    ) -> Page[CardDigestResponse]:
        q = self.session.query(CardDTO).filter_by(deck_id=deck_id)
        if only_active:
            q = q.filter_by(is_active=True)
        q = q.order_by(CardDTO.created_at.desc())

        return paginate(
            q,
            params=params,
            transformer=lambda dtos: [dto.to_response_model() for dto in dtos],
        )

    def find_by_id_and_deck_id(
        self, id: int, deck_id: int
    ) -> CardDigestResponse | None:
        dto = (
            self.session.query(CardDTO).filter_by(id=id, deck_id=deck_id).one_or_none()
        )
        return dto.to_response_model() if dto else None

    def get_random_active_by_deck_id(self, deck_id: int) -> CardDigestResponse | None:
        dto = (
            self.session.query(CardDTO)
            .filter_by(deck_id=deck_id, is_active=True)
            .order_by(func.random())
            .limit(1)
            .first()
        )
        return dto.to_response_model() if dto else None

    def count_by_deck_id(self, deck_id: int, only_active: bool | None = None) -> int:
        q = self.session.query(CardDTO).filter_by(deck_id=deck_id)
        if only_active is True:
            q = q.filter_by(is_active=True)
        elif only_active is False:
            q = q.filter_by(is_active=False)
        return q.count()

    def list_recent_by_deck_id(
        self, deck_id: int, params: Params, only_active: bool = False
    ) -> Page[CardDigestResponse]:
        q = self.session.query(CardDTO).filter_by(deck_id=deck_id)
        if only_active:
            q = q.filter_by(is_active=True)
        q = q.order_by(CardDTO.created_at.desc())
        return paginate(
            q,
            params=params,
            transformer=lambda dtos: [dto.to_response_model() for dto in dtos],
        )

    def calculate_deck_stats(self, deck_id: int) -> DeckStatsResponse:
        """Calculate comprehensive statistics for a deck."""
        now = datetime.now(timezone.utc)
        
        # Total cards
        total = self.session.query(CardDTO).filter_by(deck_id=deck_id).count()
        
        # Active and suspended
        active = self.session.query(CardDTO).filter_by(deck_id=deck_id, is_active=True).count()
        suspended = self.session.query(CardDTO).filter_by(deck_id=deck_id, suspended=True).count()
        
        # Cards by learning phase (based on repetitions)
        new_cards = self.session.query(CardDTO).filter_by(deck_id=deck_id, is_active=True, repetitions=0).count()
        learning_cards = self.session.query(CardDTO).filter(
            CardDTO.deck_id == deck_id,
            CardDTO.is_active == True,
            CardDTO.repetitions.between(1, 10)
        ).count()
        review_cards = self.session.query(CardDTO).filter(
            CardDTO.deck_id == deck_id,
            CardDTO.is_active == True,
            CardDTO.repetitions > 10
        ).count()
        
        # Due cards
        due_cards = self.session.query(CardDTO).filter(
            CardDTO.deck_id == deck_id,
            CardDTO.is_active == True,
            CardDTO.suspended == False,
            CardDTO.due_at <= now
        ).count()
        
        # Average ease (only for active cards)
        avg_ease_result = self.session.query(func.avg(CardDTO.ease_factor)).filter_by(
            deck_id=deck_id, is_active=True
        ).scalar()
        avg_ease = float(avg_ease_result) if avg_ease_result else 2.5
        
        return DeckStatsResponse(
            deck_id=deck_id,
            total_cards=total,
            active_cards=active,
            suspended_cards=suspended,
            new_cards=new_cards,
            learning_cards=learning_cards,
            review_cards=review_cards,
            due_cards=due_cards,
            average_ease=round(avg_ease, 2),
        )
