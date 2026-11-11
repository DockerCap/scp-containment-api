from fastapi import Query
from sqlalchemy import Select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models import ContainmentObject
from app.schemas import ObjectCreate, ObjectUpdate


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


def read_objects(
    session: Session, limit: int, offset: int
) -> list[ContainmentObject] | list[None]:
    statement = Select(ContainmentObject).order_by(ContainmentObject.id).limit(limit).offset(offset)
    return list[ContainmentObject](session.scalars(statement).all())


def read_object(session: Session, item_id: int) -> ContainmentObject | None:
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


def update_object(
    session: Session, item_id: int, payload: ObjectUpdate
) -> ContainmentObject | None:

    item_to_update: ContainmentObject | None = session.get(ContainmentObject, item_id)
    if item_to_update is None:
        return None
    changes = payload.model_dump(exclude_unset=True)
    if "scp_id" in changes:
        changes["scp_id"] = f"SCP-{changes["scp_id"]}"
    for key, value in changes.items():
        setattr(item_to_update, key, value)
    try:
        session.commit()
        session.refresh(item_to_update)
    except Exception:
        session.rollback()
        raise
    return item_to_update
