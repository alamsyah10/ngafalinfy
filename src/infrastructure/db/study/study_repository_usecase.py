from sqlalchemy.orm import Session

from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.domain.repository.review_log import ReviewLogRepository
from src.usecase.study.study_writeable_usecase import StudyWriteableUseCaseUnitOfWork


class StudyRepositoryUseCaseUnitOfWorkImpl(StudyWriteableUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        deck_repository: DeckRepository,
        card_repository: CardRepository,
        review_log_repository: ReviewLogRepository,
    ):
        self.session: Session = session
        self.deck_repository: DeckRepository = deck_repository
        self.card_repository: CardRepository = card_repository
        self.review_log_repository: ReviewLogRepository = review_log_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
