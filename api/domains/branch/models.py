from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass


class Branch(Base):
    __tablename__ = "Branch"

    BranchID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Address: Mapped[str] = mapped_column(String(100), nullable=False)
