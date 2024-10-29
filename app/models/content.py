from ..database.db_setup import Base
from datetime import datetime
from sqlalchemy import DateTime, Enum, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db_setup import Base


class Content(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"))
    title: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="contents")
