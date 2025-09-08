from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.domain.model.deck.deck import Deck
from src.domain.repository.deck import DeckRepository
from src.infrastructure.db.deck.deck_dto import DeckDTO


class DeckRepositoryImpl(DeckRepository):
    """
    DeckRepositoryImpl implements CRUD operations related Deck entity.
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: int, with_relation: bool = False) -> Deck | None:
        try:
            deck_dto = self.session.query(DeckDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return deck_dto.to_entity()

    def find_by_id_and_owner_id(self, id, owner_id, with_relation=False):
        try:
            deck_dto = (
                self.session.query(DeckDTO).filter_by(id=id, owner_id=owner_id).one()
            )
        except NoResultFound:
            return None
        except:
            raise

        return deck_dto.to_entity()

    def create_deck(self, deck: Deck):
        deck_dto = DeckDTO.from_entity(deck)

        try:
            self.session.add(deck_dto)
        except:
            raise

    def update_deck(self, deck: Deck):
        deck_dto = DeckDTO.from_entity(deck)
        try:
            _deck = self.session.query(DeckDTO).filter_by(id=deck.id).one()
            _deck.name = deck_dto.name
            _deck.description = deck_dto.description
            _deck.updated_at = deck_dto.updated_at
        except:
            raise

    def delete_deck_by_id(self, id: int):
        try:
            self.session.query(DeckDTO).filter_by(id=id).delete()
        except:
            raise

    def delete_deck_by_id_and_owner_id(self, id: int, owner_id: int):
        try:
            self.session.query(DeckDTO).filter_by(id=id, owner_id=owner_id).delete()
        except:
            raise
