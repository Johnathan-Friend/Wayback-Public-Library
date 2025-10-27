from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas, service
from ...db.database import get_db


router = APIRouter(
    prefix="/item_authors",
    tags=["ItemAuthors"]
)


@router.post("/", response_model=schemas.ItemAuthorRead, status_code=status.HTTP_201_CREATED)
def create_item_author(item_author: schemas.ItemAuthorCreate, db: Session = Depends(get_db)):
    new_link = service.create_item_author(db=db, item_author=item_author)
    return new_link


@router.get("/", response_model=List[schemas.ItemAuthorRead])
def read_item_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_item_authors(db, skip=skip, limit=limit)


@router.get("/{item_author_id}", response_model=schemas.ItemAuthorRead)
def read_item_author(item_author_id: int, db: Session = Depends(get_db)):
    db_link = service.get_item_author(db, item_author_id)
    if db_link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ItemAuthor link not found")
    return db_link


@router.delete("/{item_author_id}", response_model=schemas.ItemAuthorRead)
def delete_item_author(item_author_id: int, db: Session = Depends(get_db)):
    db_link = service.delete_item_author(db, item_author_id)
    if db_link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ItemAuthor link not found")
    return db_link
