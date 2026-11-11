from datetime import datetime, timezone
from enum import StrEnum
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Classification(StrEnum):
    SAFE = "Safe"
    EUCLID = "Euclid"
    KETER = "Keter"
    THAUMIEL = "Thaumiel"


class ContainmentObject(Base):

    __tablename__ = "containment_object"

    id: Mapped[int] = mapped_column(primary_key=True)
    scp_id: Mapped[str] = mapped_column(String(30), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str | None] = mapped_column(String(255))
    classification: Mapped[Classification] = mapped_column(
        SQLEnum(
            Classification,
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
            values_callable=lambda enum: [member.value for member in enum],
        )
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow
    )
