from pydantic import BaseModel


class ItemAuthorBase(BaseModel):
    ItemID: int
    AuthorID: int


class ItemAuthorCreate(ItemAuthorBase):
    pass


class ItemAuthorRead(ItemAuthorBase):
    ItemAuthorID: int

    class Config:
        from_attributes = True
