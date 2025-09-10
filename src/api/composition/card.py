from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.repository.card import CardRepository
from src.domain.repository.deck import DeckRepository
from src.infrastructure.db.card.card_query_service import CardReadableServiceImpl
from src.infrastructure.db.card.card_repository import CardRepositoryImpl
from src.infrastructure.db.card.card_repository_usecase import (
    CardRepositoryUseCaseUnitOfWorkImpl,
)
from src.infrastructure.db.core import get_session
from src.infrastructure.db.deck.deck_repository import DeckRepositoryImpl
from src.usecase.card.card_readable_service import CardReadableService
from src.usecase.card.card_readable_usecase import (
    CardReadableUseCase,
    CardReadableUseCaseImpl,
)
from src.usecase.card.card_writeable_usecase import (
    CardWriteableUseCase,
    CardWriteableUseCaseImpl,
    CardWriteableUseCaseUnitOfWork,
)


def card_read_usecase(
    session: Session = Depends(get_session),
) -> CardReadableUseCase:
    service: CardReadableService = CardReadableServiceImpl(session)
    return CardReadableUseCaseImpl(service)


def card_write_usecase(
    session: Session = Depends(get_session),
) -> CardWriteableUseCase:
    deck_repository: DeckRepository = DeckRepositoryImpl(session)
    card_repository: CardRepository = CardRepositoryImpl(session)
    uow: CardWriteableUseCaseUnitOfWork = CardRepositoryUseCaseUnitOfWorkImpl(
        session=session,
        deck_repository=deck_repository,
        card_repository=card_repository,
    )
    return CardWriteableUseCaseImpl(uow)
