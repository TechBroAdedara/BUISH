from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import DateTime, Enum, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db_setup import Base


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    length: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))
    
    # Relationships
    teacher = relationship("User", back_populates="created_courses")
    contents = relationship("Content", back_populates="course")
    quiz = relationship("Quiz", back_populates="course")
