from sqlalchemy.orm import Session

from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.usecase.card.card_writeable_usecase import CardWriteableUseCaseUnitOfWork


class CardRepositoryUseCaseUnitOfWorkImpl(CardWriteableUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        card_repository: CardRepository,
        deck_repository: DeckRepository,
    ):
        self.session: Session = session
        self.card_repository: CardRepository = card_repository
        self.deck_repository: DeckRepository = deck_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
