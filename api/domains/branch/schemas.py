from pydantic import BaseModel
from typing import Optional


class BranchBase(BaseModel):
    Address: str


class BranchCreate(BranchBase):
    pass


class BranchRead(BranchBase):
    BranchID: int

    class Config:
        from_attributes = True


class BranchUpdate(BaseModel):
    Address: Optional[str] = None
