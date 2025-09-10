from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.repository.deck import DeckRepository
from src.infrastructure.db.core import get_session
from src.infrastructure.db.deck.deck_query_service import DeckReadableServiceImpl
from src.infrastructure.db.deck.deck_repository import DeckRepositoryImpl
from src.infrastructure.db.deck.deck_repository_usecase import (
    DeckRepositoryUseCaseUnitOfWorkImpl,
)
from src.usecase.deck.deck_readable_service import (
    DeckReadableService,
)
from src.usecase.deck.deck_readable_usecase import (
    DeckReadableUseCase,
    DeckReadableUseCaseImpl,
)
from src.usecase.deck.deck_writeable_usecase import (
    DeckWriteableUseCase,
    DeckWriteableUseCaseImpl,
    DeckWriteableUseCaseUnitOfWork,
)


def deck_read_usecase(
    session: Session = Depends(get_session),
) -> DeckReadableUseCase:
    service: DeckReadableService = DeckReadableServiceImpl(session)
    return DeckReadableUseCaseImpl(service)


def deck_write_usecase(
    session: Session = Depends(get_session),
) -> DeckWriteableUseCase:
    deck_repository: DeckRepository = DeckRepositoryImpl(session)
    uow: DeckWriteableUseCaseUnitOfWork = DeckRepositoryUseCaseUnitOfWorkImpl(
        session=session, deck_repository=deck_repository
    )
    return DeckWriteableUseCaseImpl(uow)
