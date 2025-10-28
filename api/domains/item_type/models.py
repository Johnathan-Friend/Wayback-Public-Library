from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass


class ItemType(Base):
    __tablename__ = "ItemType"

    ItemTypeID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    TypeName: Mapped[str] = mapped_column(String(100), nullable=False)
