from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL = (
    "postgresql://postgres:1234@localhost:5432/ms5"
)
#DATABASE_URL = (
#    f"postgresql://{settings.POSTGRES_USER}:"
#    f"{settings.POSTGRES_PASSWORD}@"
#    f"{settings.POSTGRES_HOST}:"
#    f"{settings.POSTGRES_PORT}/"
#    f"{settings.POSTGRES_DB}"
#)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    """
    Создает сессию базы данных.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()