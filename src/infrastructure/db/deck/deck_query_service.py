from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.infrastructure.db.deck.deck_dto import DeckDTO
from src.usecase.deck.deck_readable_service import DeckReadableService


class DeckReadableServiceImpl(DeckReadableService):
    """
    DeckReadableServiceImpl implements READ operations related
    Deck entity using SQLAlchemy.
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id_and_owner_id(self, id, owner_id):
        try:
            deck_dto = (
                self.session.query(DeckDTO).filter_by(id=id, owner_id=owner_id).one()
            )
        except NoResultFound:
            return None
        except:
            raise

        return deck_dto.to_response_model()

    def list_all_by_owner_id(self, owner_id):
        return paginate(
            self.session.query(DeckDTO)
            .filter_by(owner_id=owner_id)
            .order_by(desc(DeckDTO.created_at)),
            transformer=lambda dtos: [dto.to_response_model() for dto in dtos],
        )
