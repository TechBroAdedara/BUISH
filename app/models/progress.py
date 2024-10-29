from ..database.db_setup import Base
from sqlalchemy import DateTime, Enum, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db_setup import Base
from datetime import datetime


class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    content_id: Mapped[int] = mapped_column(Integer, ForeignKey("content.id"))
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"))
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey("quiz.id"))
    status: Mapped[str] = mapped_column(
        Enum("completed", "in_progress", name="progress_status"), default="in_progress"
    )
    progress_type: Mapped[str] = mapped_column(
        Enum("content", "quiz", name="progress_type")
    )

    # relationships
    user = relationship("User", backref="progress_records")
    course = relationship("Course", backref="progress_records")
