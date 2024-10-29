from ..database.db_setup import Base
from sqlalchemy import DateTime, Enum, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db_setup import Base
from datetime import datetime


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey("quiz.id"))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(
        Enum("multiple_choice", "true_false", "short_answer", name="question_types")
    )

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="questions")
