from typing import Optional
from datetime import date
from sqlalchemy import ForeignKey, Integer, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "Transaction"

    TransactionID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ItemID: Mapped[int] = mapped_column(ForeignKey("Item.ISBN"), nullable=False)
    PatronID: Mapped[int] = mapped_column(ForeignKey("Patron.PatronID"), nullable=False)
    BranchID: Mapped[Optional[int]] = mapped_column(ForeignKey("Branch.BranchID"))
    DateStart: Mapped[date] = mapped_column(Date, nullable=False)
    DateDue: Mapped[date] = mapped_column(Date, nullable=False)
    DateReturned: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    RentalLength: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
