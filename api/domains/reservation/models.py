from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, Date, Enum, ForeignKeyConstraint, Index, Integer, String, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Branch(Base):
    __tablename__ = 'Branch'

    BranchID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Address: Mapped[str] = mapped_column(String(150), nullable=False)

    Item: Mapped[list['Item']] = relationship('Item', foreign_keys='[Item.BranchID]', back_populates='Branch_')
    Item_: Mapped[list['Item']] = relationship('Item', foreign_keys='[Item.CurrentBranchID]', back_populates='Branch1')


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

    Reservation: Mapped[list['Reservation']] = relationship('Reservation', back_populates='Patron_')


class ItemDetails(Base):
    __tablename__ = 'ItemDetails'
    __table_args__ = (
        ForeignKeyConstraint(['ItemTypeID'], ['ItemType.ItemTypeID'], ondelete='RESTRICT', onupdate='CASCADE', name='FK_ItemDetails_ItemType'),
        Index('FK_ItemDetails_ItemType', 'ItemTypeID')
    )

    ISBN: Mapped[str] = mapped_column(String(20), primary_key=True)
    ItemTypeID: Mapped[int] = mapped_column(Integer, nullable=False)
    Title: Mapped[str] = mapped_column(String(100), nullable=False)
    Price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(8, 2), nullable=False, server_default=text("'10.00'"))
    Description: Mapped[Optional[str]] = mapped_column(Text)
    Rating: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(3, 2))
    Quantity: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'1'"))

    ItemType_: Mapped['ItemType'] = relationship('ItemType', back_populates='ItemDetails')
    Item: Mapped[list['Item']] = relationship('Item', back_populates='ItemDetails_')


class Item(Base):
    __tablename__ = 'Item'
    __table_args__ = (
        ForeignKeyConstraint(['BranchID'], ['Branch.BranchID'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Item_Branch'),
        ForeignKeyConstraint(['CurrentBranchID'], ['Branch.BranchID'], name='FK_CurrentBranchID'),
        ForeignKeyConstraint(['ISBN'], ['ItemDetails.ISBN'], ondelete='RESTRICT', onupdate='CASCADE', name='FK_Item_ISBN'),
        Index('FK_CurrentBranchID', 'CurrentBranchID'),
        Index('FK_Item_Branch', 'BranchID'),
        Index('FK_Item_ISBN', 'ISBN')
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ISBN: Mapped[str] = mapped_column(String(20), nullable=False)
    BranchID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsDamaged: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    Status: Mapped[Optional[str]] = mapped_column(Enum('Available', 'Checked Out', 'Needs Reshelving', 'Reshelved'), server_default=text("'Available'"))
    CurrentBranchID: Mapped[Optional[int]] = mapped_column(Integer)

    Branch_: Mapped['Branch'] = relationship('Branch', foreign_keys=[BranchID], back_populates='Item')
    Branch1: Mapped[Optional['Branch']] = relationship('Branch', foreign_keys=[CurrentBranchID], back_populates='Item_')
    ItemDetails_: Mapped['ItemDetails'] = relationship('ItemDetails', back_populates='Item')
    Reservation: Mapped[list['Reservation']] = relationship('Reservation', back_populates='Item_')


class Reservation(Base):
    __tablename__ = 'Reservation'
    __table_args__ = (
        ForeignKeyConstraint(['ItemID'], ['Item.ItemID'], name='Reservation_ibfk_2'),
        ForeignKeyConstraint(['PatronID'], ['Patron.PatronID'], name='Reservation_ibfk_1'),
        Index('ItemID', 'ItemID'),
        Index('PatronID', 'PatronID')
    )

    ReservationID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PatronID: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReservationDate: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('(curdate())'))
    ReservationExpirationDate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    PickupDate: Mapped[Optional[datetime.date]] = mapped_column(Date)

    Item_: Mapped['Item'] = relationship('Item', back_populates='Reservation')
    Patron_: Mapped['Patron'] = relationship('Patron', back_populates='Reservation')
