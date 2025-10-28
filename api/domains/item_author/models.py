from typing import Optional
import decimal

from sqlalchemy import Column, DECIMAL, ForeignKeyConstraint, Index, Integer, String, Table, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = 'Author'

    AuthorID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FirstName: Mapped[str] = mapped_column(String(50), nullable=False)
    LastName: Mapped[str] = mapped_column(String(50), nullable=False)

    ItemDetails: Mapped[list['ItemDetails']] = relationship('ItemDetails', secondary='ItemAuthor', back_populates='Author_')


class ItemType(Base):
    __tablename__ = 'ItemType'

    ItemTypeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TypeName: Mapped[str] = mapped_column(String(50), nullable=False)
    RentalLength: Mapped[int] = mapped_column(Integer, nullable=False)
    FeeAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2), server_default=text("'0.00'"))

    ItemDetails: Mapped[list['ItemDetails']] = relationship('ItemDetails', back_populates='ItemType_')


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

    Author_: Mapped[list['Author']] = relationship('Author', secondary='ItemAuthor', back_populates='ItemDetails')
    ItemType_: Mapped['ItemType'] = relationship('ItemType', back_populates='ItemDetails')


class ItemAuthor(Base):
    __tablename__ = 'ItemAuthor'
    __table_args__ = (
        ForeignKeyConstraint(['AuthorID'], ['Author.AuthorID'], ondelete='CASCADE', onupdate='CASCADE', name='FK_ItemAuthor_Author'),
        ForeignKeyConstraint(['ISBN'], ['ItemDetails.ISBN'], ondelete='CASCADE', onupdate='CASCADE', name='FK_ItemAuthor_ISBN'),
        Index('FK_ItemAuthor_Author', 'AuthorID')
    )

    ISBN: Mapped[str] = mapped_column(String(20), primary_key=True)
    AuthorID: Mapped[int] = mapped_column(Integer, primary_key=True)

