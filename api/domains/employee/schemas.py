from pydantic import BaseModel
from typing import Optional


class EmployeeBase(BaseModel):
    FirstName: str
    LastName: str
    BranchID: Optional[int] = None
    Role: Optional[str] = None
    Address: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    EmployeeID: int

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    BranchID: Optional[int] = None
    Role: Optional[str] = None
    Address: Optional[str] = None
