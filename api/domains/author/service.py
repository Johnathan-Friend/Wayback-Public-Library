from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.AuthorID == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author_update: schemas.AuthorUpdate) -> Optional[models.Author]:
    db_author = get_author(db, author_id)
    if not db_author:
        return None

    update_data = author_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_author, key, value)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Optional[models.Author]:
    db_author = get_author(db, author_id)
    if not db_author:
        return None

    db.delete(db_author)
    db.commit()
    return db_author
