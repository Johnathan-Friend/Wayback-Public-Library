from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas, service
from ...db.database import get_db


router = APIRouter(
    prefix="/itemtypes",
    tags=["ItemType"]
)


@router.post("/", response_model=schemas.ItemTypeRead, status_code=status.HTTP_201_CREATED)
def create_itemtype(itemtype: schemas.ItemTypeCreate, db: Session = Depends(get_db)):
    return service.create_itemtype(db, itemtype)


@router.get("/", response_model=List[schemas.ItemTypeRead])
def read_itemtypes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_itemtypes(db, skip, limit)


@router.get("/{itemtype_id}", response_model=schemas.ItemTypeRead)
def read_itemtype(itemtype_id: int, db: Session = Depends(get_db)):
    db_itemtype = service.get_itemtype(db, itemtype_id)
    if db_itemtype is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ItemType not found")
    return db_itemtype


@router.patch("/{itemtype_id}", response_model=schemas.ItemTypeRead)
def update_itemtype(itemtype_id: int, itemtype_update: schemas.ItemTypeUpdate, db: Session = Depends(get_db)):
    db_itemtype = service.update_itemtype(db, itemtype_id, itemtype_update)
    if db_itemtype is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ItemType not found")
    return db_itemtype


@router.delete("/{itemtype_id}", response_model=schemas.ItemTypeRead)
def delete_itemtype(itemtype_id: int, db: Session = Depends(get_db)):
    db_itemtype = service.delete_itemtype(db, itemtype_id)
    if db_itemtype is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ItemType not found")
    return db_itemtype
