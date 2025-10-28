# app/domains/item_details/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas, service
from ...db.database import get_db

router = APIRouter(
    prefix="/item-details",
    tags=["ItemDetails"]
)

@router.post("/", response_model=schemas.ItemDetailsRead, status_code=status.HTTP_201_CREATED)
def create_item_detail(detail: schemas.ItemDetailsCreate, db: Session = Depends(get_db)):
    return service.create_item_detail(db, detail)


@router.get("/", response_model=List[schemas.ItemDetailsRead])
def read_item_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_item_details(db, skip=skip, limit=limit)


@router.get("/{detail_id}", response_model=schemas.ItemDetailsRead)
def read_item_detail(detail_id: int, db: Session = Depends(get_db)):
    db_detail = service.get_item_detail(db, detail_id)
    if not db_detail:
        raise HTTPException(status_code=404, detail="ItemDetail not found")
    return db_detail


@router.patch("/{detail_id}", response_model=schemas.ItemDetailsRead)
def update_item_detail(detail_id: int, detail_update: schemas.ItemDetailsUpdate, db: Session = Depends(get_db)):
    db_detail = service.update_item_detail(db, detail_id, detail_update)
    if not db_detail:
        raise HTTPException(status_code=404, detail="ItemDetail not found")
    return db_detail


@router.delete("/{detail_id}", response_model=schemas.ItemDetailsRead)
def delete_item_detail(detail_id: int, db: Session = Depends(get_db)):
    db_detail = service.delete_item_detail(db, detail_id)
    if not db_detail:
        raise HTTPException(status_code=404, detail="ItemDetail not found")
    return db_detail
