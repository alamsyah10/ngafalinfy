from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.domain.model.card.card import Card
from src.domain.repository.card import CardRepository
from src.infrastructure.db.card.card_dto import CardDTO


class CardRepositoryImpl(CardRepository):
    """
    CardRepositoryImpl implements CRUD & simple queries for Card entity.
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: int, with_relation: bool = False) -> Card | None:
        try:
            dto = self.session.query(CardDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise
        return dto.to_entity()

    def find_by_id_and_deck_id(
        self, id: int, deck_id: int, with_relation: bool = False
    ) -> Card | None:
        try:
            dto = self.session.query(CardDTO).filter_by(id=id, deck_id=deck_id).one()
        except NoResultFound:
            return None
        except:
            raise
        return dto.to_entity()

    def list_by_deck_id(self, deck_id: int, only_active: bool = False) -> list[Card]:
        q = self.session.query(CardDTO).filter_by(deck_id=deck_id)
        if only_active:
            q = q.filter_by(is_active=True)
        q = q.order_by(CardDTO.created_at.desc())
        return [dto.to_entity() for dto in q.all()]

    def get_random_active_by_deck_id(self, deck_id: int) -> Card | None:
        dto = (
            self.session.query(CardDTO)
            .filter_by(deck_id=deck_id, is_active=True)
            .order_by(func.random())
            .limit(1)
            .first()
        )
        return dto.to_entity() if dto else None

    def create_card(self, card: Card):
        dto = CardDTO.from_entity(card)
        try:
            self.session.add(dto)
        except:
            raise

    def update_card(self, card: Card):
        try:
            row = self.session.query(CardDTO).filter_by(id=card.id).one()
            row.front = card.front
            row.back = card.back
            row.notes = card.notes
            row.is_active = card.is_active
            row.updated_at = card.updated_at
        except:
            raise

    def delete_card_by_id(self, id: int):
        try:
            self.session.query(CardDTO).filter_by(id=id).delete()
        except:
            raise

    def delete_card_by_id_and_deck_id(self, id: int, deck_id: int):
        try:
            self.session.query(CardDTO).filter_by(id=id, deck_id=deck_id).delete()
        except:
            raise
