from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.domain.repository.review_log import ReviewLogRepository
from src.infrastructure.db.card.card_repository import CardRepositoryImpl
from src.infrastructure.db.core import get_session
from src.infrastructure.db.deck.deck_repository import DeckRepositoryImpl
from src.infrastructure.db.review_log.review_log_query_service import (
    ReviewLogReadableServiceImpl,
)
from src.infrastructure.db.review_log.review_log_repository import ReviewLogRepositoryImpl
from src.infrastructure.db.review_log.review_log_repository_usecase import (
    ReviewLogRepositoryUseCaseUnitOfWorkImpl,
)
from src.usecase.review_log.review_log_readable_service import ReviewLogReadableService
from src.usecase.review_log.review_log_readable_usecase import (
    ReviewLogReadableUseCase,
    ReviewLogReadableUseCaseImpl,
)
from src.usecase.review_log.review_log_writeable_usecase import (
    ReviewLogWriteableUseCase,
    ReviewLogWriteableUseCaseImpl,
    ReviewLogWriteableUseCaseUnitOfWork,
)


def review_log_read_usecase(
    session: Session = Depends(get_session),
) -> ReviewLogReadableUseCase:
    service: ReviewLogReadableService = ReviewLogReadableServiceImpl(session)
    return ReviewLogReadableUseCaseImpl(service)


def review_log_write_usecase(
    session: Session = Depends(get_session),
) -> ReviewLogWriteableUseCase:
    deck_repository: DeckRepository = DeckRepositoryImpl(session)
    card_repository: CardRepository = CardRepositoryImpl(session)
    review_log_repository: ReviewLogRepository = ReviewLogRepositoryImpl(session)

    uow: ReviewLogWriteableUseCaseUnitOfWork = ReviewLogRepositoryUseCaseUnitOfWorkImpl(
        session=session,
        deck_repository=deck_repository,
        card_repository=card_repository,
        review_log_repository=review_log_repository,
    )
    return ReviewLogWriteableUseCaseImpl(uow)
