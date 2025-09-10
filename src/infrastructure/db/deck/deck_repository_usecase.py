from sqlalchemy.orm import Session

from src.domain.repository.deck import DeckRepository
from src.usecase.deck.deck_writeable_usecase import DeckWriteableUseCaseUnitOfWork


class DeckRepositoryUseCaseUnitOfWorkImpl(DeckWriteableUseCaseUnitOfWork):
    def __init__(self, session: Session, deck_repository: DeckRepository):
        self.session: Session = session
        self.deck_repository: DeckRepository = deck_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
