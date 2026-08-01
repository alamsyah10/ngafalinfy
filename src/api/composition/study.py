from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.domain.repository.review_log import ReviewLogRepository
from src.infrastructure.db.card.card_repository import CardRepositoryImpl
from src.infrastructure.db.core import get_session
from src.infrastructure.db.deck.deck_repository import DeckRepositoryImpl
from src.infrastructure.db.review_log.review_log_repository import ReviewLogRepositoryImpl
from src.infrastructure.db.study.study_repository_usecase import (
    StudyRepositoryUseCaseUnitOfWorkImpl,
)
from src.usecase.study.study_writeable_usecase import (
    StudyWriteableUseCase,
    StudyWriteableUseCaseImpl,
    StudyWriteableUseCaseUnitOfWork,
)


def study_write_usecase(
    session: Session = Depends(get_session),
) -> StudyWriteableUseCase:
    deck_repository: DeckRepository = DeckRepositoryImpl(session)
    card_repository: CardRepository = CardRepositoryImpl(session)
    review_log_repository: ReviewLogRepository = ReviewLogRepositoryImpl(session)

    uow: StudyWriteableUseCaseUnitOfWork = StudyRepositoryUseCaseUnitOfWorkImpl(
        session=session,
        deck_repository=deck_repository,
        card_repository=card_repository,
        review_log_repository=review_log_repository,
    )
    return StudyWriteableUseCaseImpl(uow)
