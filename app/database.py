from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


DATABASE_PATH = Path(__file__).resolve().parent.parent / "app.db"
engine = create_engine(URL.create("sqlite+pysqlite", database=str(DATABASE_PATH)))

SessionLocal = sessionmaker(engine)


def get_db() -> Iterator[Session]:
    with SessionLocal() as db:
        yield db
