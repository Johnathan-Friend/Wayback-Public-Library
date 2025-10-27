# app/domains/item_details/service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_item_detail(db: Session, detail_id: int) -> Optional[models.ItemDetail]:
    return db.query(models.ItemDetail).filter(models.ItemDetail.DetailID == detail_id).first()


def get_item_details(db: Session, skip: int = 0, limit: int = 100) -> List[models.ItemDetail]:
    return db.query(models.ItemDetail).offset(skip).limit(limit).all()


def create_item_detail(db: Session, detail: schemas.ItemDetailCreate) -> models.ItemDetail:
    db_detail = models.ItemDetail(**detail.model_dump())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail


def update_item_detail(db: Session, detail_id: int, detail_update: schemas.ItemDetailUpdate) -> Optional[models.ItemDetail]:
    db_detail = get_item_detail(db, detail_id)
    if not db_detail:
        return None
    update_data = detail_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_detail, key, value)
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail


def delete_item_detail(db: Session, detail_id: int) -> Optional[models.ItemDetail]:
    db_detail = get_item_detail(db, detail_id)
    if not db_detail:
        return None
    db.delete(db_detail)
    db.commit()
    return db_detail
