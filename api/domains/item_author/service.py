from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

def get_item_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.ItemAuthor]:
    return db.query(models.ItemAuthor).offset(skip).limit(limit).all()

def get_item_authors_by_isbn(db: Session, isbn: str) -> List[models.ItemAuthor]:
    """
    Gets all ItemAuthor link entries for a specific ISBN.
    (i.e., finds all authors for a single book)
    """
    return db.query(models.ItemAuthor).filter(models.ItemAuthor.ISBN == isbn).all()

def get_item_authors_by_author(db: Session, author_id: int) -> List[models.ItemAuthor]:
    """
    Gets all ItemAuthor link entries for a specific AuthorID.
    (i.e., finds all books for a single author)
    """
    return db.query(models.ItemAuthor).filter(models.ItemAuthor.AuthorID == author_id).all()

def get_item_author_link(db: Session, isbn: str, author_id: int) -> Optional[models.ItemAuthor]:
    """
    Finds one specific link by its composite primary key.
    """
    return db.query(models.ItemAuthor).filter(
        models.ItemAuthor.ISBN == isbn,
        models.ItemAuthor.AuthorID == author_id
    ).first()

def create_item_author(db: Session, item_author: schemas.ItemAuthorCreate) -> models.ItemAuthor:
    db_item_author = models.ItemAuthor(**item_author.model_dump())
    db.add(db_item_author)
    db.commit()
    db.refresh(db_item_author)
    return db_item_author


def delete_item_author(db: Session, isbn: str, item_author_id: int) -> Optional[models.ItemAuthor]:
    db_item_author = get_item_author_link(db, isbn, item_author_id)
    if not db_item_author:
        return None
    db.delete(db_item_author)
    db.commit()
    return db_item_author
