from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

class Base(DeclarativeBase):
    pass


class ItemAuthor(Base):
    __tablename__ = "ItemAuthor"

    ItemAuthorID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ItemID: Mapped[int] = mapped_column(ForeignKey("Item.ItemID"), nullable=False)
    AuthorID: Mapped[int] = mapped_column(ForeignKey("Author.AuthorID"), nullable=False)
