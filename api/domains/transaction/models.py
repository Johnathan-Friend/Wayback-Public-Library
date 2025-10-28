from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, Date, ForeignKeyConstraint, Index, Integer, String, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Branch(Base):
    __tablename__ = 'Branch'

    BranchID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Address: Mapped[str] = mapped_column(String(150), nullable=False)

    Item: Mapped[list['Item']] = relationship('Item', back_populates='Branch_')
    Transactions: Mapped[list['Transactions']] = relationship('Transactions', back_populates='Branch_')


class ItemType(Base):
    __tablename__ = 'ItemType'

    ItemTypeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TypeName: Mapped[str] = mapped_column(String(50), nullable=False)
    RentalLength: Mapped[int] = mapped_column(Integer, nullable=False)
    FeeAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2), server_default=text("'0.00'"))

    ItemDetails: Mapped[list['ItemDetails']] = relationship('ItemDetails', back_populates='ItemType_')


class Patron(Base):
    __tablename__ = 'Patron'

    PatronID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FirstName: Mapped[str] = mapped_column(String(50), nullable=False)
    LastName: Mapped[str] = mapped_column(String(50), nullable=False)
    MembershipExpiration: Mapped[Optional[datetime.date]] = mapped_column(Date)
    FeeBalance: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2), server_default=text("'0.00'"))

    Transactions: Mapped[list['Transactions']] = relationship('Transactions', back_populates='Patron_')


class ItemDetails(Base):
    __tablename__ = 'ItemDetails'
    __table_args__ = (
        ForeignKeyConstraint(['ItemTypeID'], ['ItemType.ItemTypeID'], ondelete='RESTRICT', onupdate='CASCADE', name='FK_ItemDetails_ItemType'),
        Index('FK_ItemDetails_ItemType', 'ItemTypeID')
    )

    ISBN: Mapped[str] = mapped_column(String(20), primary_key=True)
    ItemTypeID: Mapped[int] = mapped_column(Integer, nullable=False)
    Title: Mapped[str] = mapped_column(String(100), nullable=False)
    Description: Mapped[Optional[str]] = mapped_column(Text)
    Rating: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(3, 2))
    Quantity: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'1'"))

    ItemType_: Mapped['ItemType'] = relationship('ItemType', back_populates='ItemDetails')
    Item: Mapped[list['Item']] = relationship('Item', back_populates='ItemDetails_')


class Item(Base):
    __tablename__ = 'Item'
    __table_args__ = (
        ForeignKeyConstraint(['BranchID'], ['Branch.BranchID'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Item_Branch'),
        ForeignKeyConstraint(['ISBN'], ['ItemDetails.ISBN'], ondelete='RESTRICT', onupdate='CASCADE', name='FK_Item_ISBN'),
        Index('FK_Item_Branch', 'BranchID'),
        Index('FK_Item_ISBN', 'ISBN')
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ISBN: Mapped[str] = mapped_column(String(20), nullable=False)
    BranchID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsDamaged: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))

    Branch_: Mapped['Branch'] = relationship('Branch', back_populates='Item')
    ItemDetails_: Mapped['ItemDetails'] = relationship('ItemDetails', back_populates='Item')
    Transactions: Mapped[list['Transactions']] = relationship('Transactions', back_populates='Item_')


class Transactions(Base):
    __tablename__ = 'Transactions'
    __table_args__ = (
        ForeignKeyConstraint(['ItemID'], ['Item.ItemID'], ondelete='RESTRICT', onupdate='CASCADE', name='FK_Transactions_Item'),
        ForeignKeyConstraint(['PatronID'], ['Patron.PatronID'], ondelete='RESTRICT', onupdate='CASCADE', name='FK_Transactions_Patron'),
        ForeignKeyConstraint(['ReturnedBranchID'], ['Branch.BranchID'], ondelete='SET NULL', onupdate='CASCADE', name='FK_Transactions_Branch'),
        Index('FK_Transactions_Branch', 'ReturnedBranchID'),
        Index('FK_Transactions_Item', 'ItemID'),
        Index('FK_Transactions_Patron', 'PatronID')
    )

    TransactionID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PatronID: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    DateStart: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    DateDue: Mapped[Optional[datetime.date]] = mapped_column(Date)
    DateReturned: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ReturnedBranchID: Mapped[Optional[int]] = mapped_column(Integer)

    Item_: Mapped['Item'] = relationship('Item', back_populates='Transactions')
    Patron_: Mapped['Patron'] = relationship('Patron', back_populates='Transactions')
    Branch_: Mapped[Optional['Branch']] = relationship('Branch', back_populates='Transactions')
