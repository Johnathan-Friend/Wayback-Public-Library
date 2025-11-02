from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal


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

class PatronTransactions(BaseModel):
    TransactionID: int
    PatronID: int
    ItemID: int
    DateStart: date
    DateDue: date
    DateReturned: Optional[date]
    ReturnedBranchID: Optional[int]
    ISBN: str
    Title: str
    Description: Optional[str]
    TypeName: str

class TransactionUpdate(BaseModel):
    ItemID: Optional[int] = None
    PatronID: Optional[int] = None
    BranchID: Optional[int] = None
    DateStart: Optional[date] = None
    DateDue: Optional[date] = None
    DateReturned: Optional[date] = None
    RentalLength: Optional[int] = None

class ItemReturnRequest(BaseModel):
    patron_id: int
    item_id: int
    return_date: date

class ItemReturnResponse(BaseModel):
    Status: str
    PatronID: int
    PatronName: str
    TransactionID: int
    ItemID: int
    DateCheckedOut: date
    DateDue: Optional[date]
    DateReturned: date
    DaysLate: int
    FeeCharged: Decimal
    UpdatedBalance: Decimal

    class Config:
        from_attributes = True