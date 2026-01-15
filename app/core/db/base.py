from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, DateTime
from uuid6 import uuid7


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now()
    )


class UUIDv7Mixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid7,
        unique=True, nullable=False
    )
