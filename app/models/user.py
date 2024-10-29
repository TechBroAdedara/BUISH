from datetime import datetime
from ..database.db_setup import Base
from sqlalchemy import TIMESTAMP, DateTime, Enum, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        Enum("student", "admin", "teacher", name="user_roles"), default="student"
    )
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    is_verified: Mapped[str] = mapped_column(Boolean, default=False)

    # Relationships
    courses = relationship("Enrollment", back_populates="user")

