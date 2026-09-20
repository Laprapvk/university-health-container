from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campuses.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    code: Mapped[str | None] = mapped_column(String(30), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30))
    campus = relationship("Campus", back_populates="departments")
    services = relationship("Service", back_populates="department", cascade="all, delete-orphan")
    staff_members = relationship("StaffMember", back_populates="department", cascade="all, delete-orphan")
