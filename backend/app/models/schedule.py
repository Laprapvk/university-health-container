from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.service import Service


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    opening_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    closing_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    service: Mapped[Service] = relationship(back_populates="schedules")
