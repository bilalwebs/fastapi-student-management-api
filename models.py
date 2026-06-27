

# models.py
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=True)

    age: Mapped[int] = mapped_column(nullable=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    department: Mapped[str] = mapped_column(nullable=False)

    password: Mapped[str] = mapped_column(nullable=False)
