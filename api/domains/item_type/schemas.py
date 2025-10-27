from pydantic import BaseModel


class ItemTypeBase(BaseModel):
    TypeName: str


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeRead(ItemTypeBase):
    ItemTypeID: int

    class Config:
        from_attributes = True  # for ORM → schema conversion


class ItemTypeUpdate(BaseModel):
    TypeName: str | None = None
