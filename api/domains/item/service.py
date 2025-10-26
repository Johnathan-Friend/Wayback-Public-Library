# app/domains/items/service.py

from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# -----------------
# --- READ (One)
# -----------------
def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """
    Get a single item by its ItemID.
    """
    return db.query(models.Item).filter(models.Item.ItemID == item_id).first()


# -----------------
# --- READ (Many)
# -----------------
def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """
    Get a list of all items with pagination.
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


# -----------------
# --- CREATE
# -----------------
def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    """
    Create a new item in the database.
    """
    db_item = models.Item(**item.model_dump())

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# -----------------
# --- UPDATE
# -----------------
def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate) -> Optional[models.Item]:
    """
    Update an existing item's information.
    """
    db_item = get_item(db, item_id)

    if not db_item:
        return None  # The item doesn't exist

    update_data = item_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# -----------------
# --- DELETE
# -----------------
def delete_item(db: Session, item_id: int) -> Optional[models.Item]:
    """
    Delete an item from the database.
    """
    db_item = get_item(db, item_id)

    if not db_item:
        return None  # The item doesn't exist

    db.delete(db_item)
    db.commit()
    return db_item
