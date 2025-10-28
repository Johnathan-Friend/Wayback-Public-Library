from pydantic import BaseModel
from typing import Optional


class AuthorBase(BaseModel):
    FirstName: str
    LastName: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    AuthorID: int

    class Config:
        from_attributes = True


class AuthorUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
