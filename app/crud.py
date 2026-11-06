from sqlalchemy import Select
from sqlalchemy.orm import Session

from app.models import ContainmentObject
from app.schemas import ObjectCreate


def create_item(session: Session, payload:ObjectCreate) -> ContainmentObject:
    record: ContainmentObject = ContainmentObject(
        scp_id= f'SCP-{str(payload.scp_id)}',
        name = payload.name,
        description = payload.description,
        classification = payload.classification
    )
    session.add(record)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(record)
    return record
    