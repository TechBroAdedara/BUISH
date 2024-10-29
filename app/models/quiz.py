from ..database.db_setup import Base
from sqlalchemy import DateTime, Enum, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db_setup import Base
from datetime import datetime


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relationship
    course = relationship("Course", back_populates="quiz")
    questions = relationship("Question", back_populates="quiz")
