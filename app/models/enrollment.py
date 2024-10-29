from ..database.db_setup import Base
from sqlalchemy import DateTime, Enum, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db_setup import Base
from datetime import datetime


class Enrollment(Base):
    __tablename__ = "enrollment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"))
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="courses")
