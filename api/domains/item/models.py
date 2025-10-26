from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, Date, Integer, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "Item"

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Title: Mapped[str] = mapped_column(String(100), nullable=False)
    Author: Mapped[Optional[str]] = mapped_column(String(100))
    ISBN: Mapped[Optional[str]] = mapped_column(String(20))
    Genre: Mapped[Optional[str]] = mapped_column(String(50))
    PublishDate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    CopiesAvailable: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("1"))
