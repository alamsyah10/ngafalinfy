from sqlalchemy.orm import Session

from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.domain.repository.review_log import ReviewLogRepository
from src.usecase.review_log.review_log_writeable_usecase import (
    ReviewLogWriteableUseCaseUnitOfWork
)


class ReviewLogRepositoryUseCaseUnitOfWorkImpl(ReviewLogWriteableUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        review_log_repository: ReviewLogRepository,
        card_repository: CardRepository,
        deck_repository: DeckRepository,
    ):
        self.session: Session = session
        self.review_log_repository: ReviewLogRepository = review_log_repository
        self.card_repository: CardRepository = card_repository
        self.deck_repository: DeckRepository = deck_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
