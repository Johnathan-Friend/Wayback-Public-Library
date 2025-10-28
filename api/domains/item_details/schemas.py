# app/domains/item_details/schemas.py
from pydantic import BaseModel
from typing import Optional


class ItemDetailsBase(BaseModel):
    ItemTypeID: int
    Title: Optional[str] = None
    Description: Optional[str] = None
    Rating: Optional[float] = None
    Quantity: Optional[int] = None


class ItemDetailsCreate(ItemDetailsBase):
    pass


class ItemDetailsRead(ItemDetailsBase):
    ISBN: str

    class Config:
        from_attributes = True


class ItemDetailsUpdate(BaseModel):
    ItemTypeID: Optional[int] = None
    Title: Optional[str] = None
    Description: Optional[str] = None
    Rating: Optional[float] = None
    Quantity: Optional[int] = None
