from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    service = relationship("Service", back_populates="contacts")
