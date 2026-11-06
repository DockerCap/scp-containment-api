from collections.abc import Iterator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine(url='sqlite+pysqlite:///app.db')

SessionLocal = sessionmaker(engine)
session = SessionLocal()
Base.metadata.create_all(engine)




def get_db() -> Iterator[Session]:
    with SessionLocal() as db:
        yield db
