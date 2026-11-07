from sqlalchemy import Select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models import ContainmentObject
from app.schemas import ObjectCreate


def create_object(session: Session, payload: ObjectCreate) -> ContainmentObject:
    record: ContainmentObject = ContainmentObject(
        scp_id=f"SCP-{str(payload.scp_id)}",
        name=payload.name,
        description=payload.description,
        classification=payload.classification,
    )
    session.add(record)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(record)
    return record


def list_objects(session: Session) -> list[ContainmentObject]:
    statement = Select(ContainmentObject)
    return list[ContainmentObject](session.scalars(statement).all())


def get_object(session: Session, item_id: int) -> ContainmentObject | None:
    return session.get(ContainmentObject, item_id)


def delete_object(session: Session, item_id: int) -> bool:
    try:
        item_to_delete: ContainmentObject | None = session.get(
            ContainmentObject, item_id
        )
        if item_to_delete is None:
            return False
        session.delete(item_to_delete)
        session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        raise

def update_object(session: Session, payload: ContainmentObject)