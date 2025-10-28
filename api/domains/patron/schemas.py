# app/domains/patrons/schemas.py
# Gemini Assisted Code for Example

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# 1. Base schema: Common fields
class PatronBase(BaseModel):
    FirstName: str
    LastName: str
    MembershipExpiration: Optional[date] = None
    FeeBalance: Optional[float] = Field(default=0.0)

# 2. Create schema: Used for POST
class PatronCreate(PatronBase):
    # This assumes PatronID is NOT set by the client, but by the DB
    # If PatronID IS set by the client (like a student ID), add it here:
    # PatronID: int
    pass

# 3. Read schema: Used for GET
class PatronRead(PatronBase):
    PatronID: int  # The DB-generated primary key

    class Config:
        from_attributes = True # This is the Pydantic v2+ way (you had orm_mode)

# 4. Update schema: Used for PATCH
class PatronUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    MembershipExpiration: Optional[date] = None
    FeeBalance: Optional[float] = None
