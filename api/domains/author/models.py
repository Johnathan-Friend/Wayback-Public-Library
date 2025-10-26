from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "Author"

    AuthorID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    FirstName: Mapped[str] = mapped_column(String(50), nullable=False)
    LastName: Mapped[str] = mapped_column(String(50), nullable=False)
