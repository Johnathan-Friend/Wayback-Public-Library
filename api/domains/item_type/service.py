from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_itemtype(db: Session, itemtype_id: int) -> Optional[models.ItemType]:
    return db.query(models.ItemType).filter(models.ItemType.ItemTypeID == itemtype_id).first()


def get_itemtypes(db: Session, skip: int = 0, limit: int = 100) -> List[models.ItemType]:
    return db.query(models.ItemType).offset(skip).limit(limit).all()


def create_itemtype(db: Session, itemtype: schemas.ItemTypeCreate) -> models.ItemType:
    db_itemtype = models.ItemType(**itemtype.model_dump())
    db.add(db_itemtype)
    db.commit()
    db.refresh(db_itemtype)
    return db_itemtype


def update_itemtype(db: Session, itemtype_id: int, itemtype_update: schemas.ItemTypeUpdate) -> Optional[models.ItemType]:
    db_itemtype = get_itemtype(db, itemtype_id)
    if not db_itemtype:
        return None
    update_data = itemtype_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_itemtype, key, value)
    db.add(db_itemtype)
    db.commit()
    db.refresh(db_itemtype)
    return db_itemtype


def delete_itemtype(db: Session, itemtype_id: int) -> Optional[models.ItemType]:
    db_itemtype = get_itemtype(db, itemtype_id)
    if not db_itemtype:
        return None
    db.delete(db_itemtype)
    db.commit()
    return db_itemtype
