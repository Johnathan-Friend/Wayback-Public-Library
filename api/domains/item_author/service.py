from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_item_author(db: Session, item_author_id: int) -> Optional[models.ItemAuthor]:
    return db.query(models.ItemAuthor).filter(models.ItemAuthor.ItemAuthorID == item_author_id).first()


def get_item_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.ItemAuthor]:
    return db.query(models.ItemAuthor).offset(skip).limit(limit).all()


def create_item_author(db: Session, item_author: schemas.ItemAuthorCreate) -> models.ItemAuthor:
    db_item_author = models.ItemAuthor(**item_author.model_dump())
    db.add(db_item_author)
    db.commit()
    db.refresh(db_item_author)
    return db_item_author


def delete_item_author(db: Session, item_author_id: int) -> Optional[models.ItemAuthor]:
    db_item_author = get_item_author(db, item_author_id)
    if not db_item_author:
        return None
    db.delete(db_item_author)
    db.commit()
    return db_item_author
