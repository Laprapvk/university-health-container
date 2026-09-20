from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"), index=True)
    building_id: Mapped[int | None] = mapped_column(ForeignKey("buildings.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100), index=True)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30))
    website: Mapped[str | None] = mapped_column(String(255))
    department = relationship("Department", back_populates="services")
    building = relationship("Building", back_populates="services")
    contacts = relationship("Contact", back_populates="service", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="service", cascade="all, delete-orphan")
