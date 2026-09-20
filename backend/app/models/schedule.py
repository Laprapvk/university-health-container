from sqlalchemy import ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), index=True)
    day_of_week: Mapped[str] = mapped_column(String(20))
    opening_time: Mapped[object | None] = mapped_column(Time)
    closing_time: Mapped[object | None] = mapped_column(Time)
    service = relationship("Service", back_populates="schedules")
