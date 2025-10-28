from pydantic import BaseModel


class ItemAuthorBase(BaseModel):
    ISBN: str
    AuthorID: int


class ItemAuthorCreate(ItemAuthorBase):
    pass


class ItemAuthorRead(ItemAuthorBase):
    AuthorID: int

    class Config:
        from_attributes = True
