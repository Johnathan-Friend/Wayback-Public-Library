from pydantic import BaseModel
from datetime import date
from typing import Optional


class TransactionBase(BaseModel):
    ItemID: int
    PatronID: int
    BranchID: Optional[int] = None
    DateStart: date
    DateDue: date
    DateReturned: Optional[date] = None
    RentalLength: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    TransactionID: int

    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    ItemID: Optional[int] = None
    PatronID: Optional[int] = None
    BranchID: Optional[int] = None
    DateStart: Optional[date] = None
    DateDue: Optional[date] = None
    DateReturned: Optional[date] = None
    RentalLength: Optional[int] = None
