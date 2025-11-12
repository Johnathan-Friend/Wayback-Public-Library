from pydantic import BaseModel
from datetime import date
from typing import Optional


class ReservationBase(BaseModel):
    ItemID: int
    PatronID: int
    ReservationDate: Optional[date] = None
    ReservationExpirationDate: Optional[date]
    PickupDate: Optional[date]

    class Config:
        orm_mode = True

class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    ReservationID: int

    class Config:
        from_attributes = True  # Enables ORM integration (replaces orm_mode in Pydantic v2)

class ReservationUpdate(BaseModel):
    ItemID: Optional[int]
    PatronID: Optional[int]
    ReservationDate: Optional[date]
    ReservationExpirationDate: Optional[date]
    PickupDate: Optional[date]