# app/domains/item_details/schemas.py
from pydantic import BaseModel
from typing import Optional


class ItemDetailBase(BaseModel):
    ItemID: int
    ISBN: Optional[str] = None
    Publisher: Optional[str] = None
    Language: Optional[str] = None
    Edition: Optional[str] = None
    Description: Optional[str] = None


class ItemDetailCreate(ItemDetailBase):
    pass


class ItemDetailRead(ItemDetailBase):
    DetailID: int

    class Config:
        from_attributes = True


class ItemDetailUpdate(BaseModel):
    ISBN: Optional[str] = None
    Publisher: Optional[str] = None
    Language: Optional[str] = None
    Edition: Optional[str] = None
    Description: Optional[str] = None
