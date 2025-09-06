from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from src.config import settings

engine = create_engine(
    settings.get_database_url(),
    connect_args=settings.get_database_args(),
    echo=settings.SQL_LOGGING,
    pool_pre_ping=True,
)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


def get_session():
    session: Session = db_session()
    try:
        yield session
    finally:
        session.close()
