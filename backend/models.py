from datetime import date as Date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    contact: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user",
    )


class Task(Base):
    __tablename__ = "tarefas"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    times_per_week: Mapped[int] = mapped_column(nullable=False)
    first_date: Mapped[Date] = mapped_column(nullable=False)
    date: Mapped[Date] = mapped_column(nullable=False)

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )