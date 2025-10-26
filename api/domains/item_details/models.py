# app/domains/item_details/models.py
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class ItemDetail(Base):
    __tablename__ = "ItemDetail"

    DetailID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ItemID: Mapped[int] = mapped_column(ForeignKey("Item.ItemID"), nullable=False)
    ISBN: Mapped[Optional[str]] = mapped_column(String(20))
    Publisher: Mapped[Optional[str]] = mapped_column(String(100))
    Language: Mapped[Optional[str]] = mapped_column(String(50))
    Edition: Mapped[Optional[str]] = mapped_column(String(50))
    Description: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationship
    item = relationship("Item", back_populates="details")
